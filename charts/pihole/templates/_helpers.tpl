{{/* vim: set filetype=mustache: */}}
{{/*
Expand the name of the chart.
*/}}
{{- define "pihole.name" -}}
{{- default .Chart.Name .Values.nameOverride | trunc 63 | trimSuffix "-" -}}
{{- end -}}

{{/*
Create a default fully qualified app name.
We truncate at 63 chars because some Kubernetes name fields are limited to this (by the DNS naming spec).
If release name contains chart name it will be used as a full name.
*/}}
{{- define "pihole.fullname" -}}
{{- if .Values.fullnameOverride -}}
{{- .Values.fullnameOverride | trunc 63 | trimSuffix "-" -}}
{{- else -}}
{{- $name := default .Chart.Name .Values.nameOverride -}}
{{- if contains $name .Release.Name -}}
{{- .Release.Name | trunc 63 | trimSuffix "-" -}}
{{- else -}}
{{- printf "%s-%s" .Release.Name $name | trunc 63 | trimSuffix "-" -}}
{{- end -}}
{{- end -}}
{{- end -}}

{{/*
Create chart name and version as used by the chart label.
*/}}
{{- define "pihole.chart" -}}
{{- printf "%s-%s" .Chart.Name .Chart.Version | replace "+" "_" | trunc 63 | trimSuffix "-" -}}
{{- end -}}

{{/*
Default password secret name.
*/}}
{{- define "pihole.password-secret" -}}
{{- printf "%s-%s" (include "pihole.fullname" .) "password" | replace "+" "_" | trunc 63 | trimSuffix "-" -}}
{{- end -}}

{{/*
Common labels
*/}}
{{- define "pihole.labels" -}}
helm.sh/chart: {{ include "pihole.chart" . }}
{{ include "pihole.selectorLabels" . }}
{{- if .Chart.AppVersion }}
app.kubernetes.io/version: {{ .Chart.AppVersion | quote }}
{{- end }}
app.kubernetes.io/managed-by: {{ .Release.Service }}
{{- with .Values.commonLabels }}
{{ toYaml . }}
{{- end }}
{{- end }}

{{/*
Selector labels
*/}}
{{- define "pihole.selectorLabels" -}}
app.kubernetes.io/name: {{ include "pihole.name" . }}
app.kubernetes.io/instance: {{ .Release.Name }}
{{- end }}

{{/*
Create the name of the service account to use
*/}}
{{- define "pihole.serviceAccountName" -}}
{{- if .Values.serviceAccount.create }}
{{- default (include "pihole.fullname" .) .Values.serviceAccount.name }}
{{- else }}
{{- default "default" .Values.serviceAccount.name }}
{{- end }}
{{- end }}

{{/*
Default health check for the Pi-hole container, used by all probes of type "command".
It only checks Pi-hole itself (API up and FTL answering pi.hole without recursion),
never an upstream resolver, so an internet outage does not restart Pi-hole.
dig exits 0 even on SERVFAIL, therefore a non-empty answer is required.
Every step has its own timeout (max ~4s) so the probe never outlives timeoutSeconds:
a hanging exec probe stalls the kubelet and the container would never be restarted.
With redirectToHttps the HTTP port only answers with redirects, so the API is called via
HTTPS (-k: Pi-hole's own certificate is self-signed, and this is the pod talking to itself).
*/}}
{{- define "pihole.probeCommand" -}}
{{- if and .Values.webHttps .Values.redirectToHttps -}}
curl -skf --max-time 2 https://localhost:{{ .Values.webHttps }}/api/info/login
{{- else -}}
curl -sf --max-time 2 http://localhost:{{ .Values.webHttp }}/api/info/login
{{- end }} | jq -e '.dns == true' >/dev/null && [ -n "$(dig +short +norecurse +retry=0 +time=2 -p {{ .Values.dnsPort }} @127.0.0.1 pi.hole)" ]
{{- end }}

{{/*
Dual stack. Call with (dict "root" $ "svc" .Values.serviceXyz).
"pihole.splitIPv6" is non-empty when a LoadBalancer service is split into an IPv4 and a separate
"-ipv6" service (dualStack.splitLoadBalancer: true). By default it is one dual-stack service.
*/}}
{{- define "pihole.splitIPv6" -}}
{{- if and .root.Values.dualStack.enabled (eq .svc.type "LoadBalancer") -}}
{{- if .root.Values.dualStack.splitLoadBalancer -}}
true
{{- else if .svc.loadBalancerIPv6 -}}
{{- fail "loadBalancerIPv6 needs dualStack.splitLoadBalancer: true. For a single dual-stack LoadBalancer service, put both addresses into your load balancer's annotation (e.g. metallb.universe.tf/loadBalancerIPs: \"192.168.1.53,fd00::53\")" -}}
{{- end -}}
{{- end -}}
{{- end }}

{{/*
ipFamilies of the main service. When split, it is pinned to IPv4 so it gets an IPv4 address
even on IPv6-primary clusters; otherwise it is a single dual-stack service.
*/}}
{{- define "pihole.ipFamilies" -}}
{{- if .root.Values.dualStack.enabled -}}
{{- if include "pihole.splitIPv6" . -}}
ipFamilies:
  - IPv4
ipFamilyPolicy: SingleStack
{{- else -}}
ipFamilies:
  - IPv4
  - IPv6
ipFamilyPolicy: PreferDualStack
{{- end -}}
{{- end -}}
{{- end }}

{{/*
Metadata labels and annotations of the "-ipv6" service: the service's extraLabels and its
annotations, overridden key by key by annotationsIPv6 (e.g. a different IP for Cilium LB IPAM or MetalLB).
*/}}
{{- define "pihole.ipv6Metadata" -}}
labels:
  {{- include "pihole.labels" .root | nindent 2 }}
  {{- with .svc.extraLabels }}
  {{- toYaml . | nindent 2 }}
  {{- end }}
{{- with merge (deepCopy (.svc.annotationsIPv6 | default dict)) (.svc.annotations | default dict) }}
annotations:
  {{- toYaml . | nindent 2 }}
{{- end }}
{{- end }}

{{/*
Deployment strategy. With persistent storage two Pi-holes would share one gravity.db, and with
hostNetwork/dnsHostPort the new pod cannot start while the old one holds the ports, so these use Recreate.
*/}}
{{- define "pihole.strategyType" -}}
{{- if .Values.strategyType -}}
{{ .Values.strategyType }}
{{- else if or .Values.persistentVolumeClaim.enabled .Values.customVolumes.enabled .Values.dnsHostPort.enabled (and .Values.hostNetwork (ne (toString .Values.hostNetwork) "false")) -}}
Recreate
{{- else -}}
RollingUpdate
{{- end -}}
{{- end }}

{{/*
Non-empty when Pi-hole's NTP client (ntp.sync.active) is on: ftl.ntp_sync_active or
extraEnvVars.FTLCONF_ntp_sync_active when set, otherwise ntp.sync.
A valueFrom can't be evaluated here and counts as off.
*/}}
{{- define "pihole.ntpSync" -}}
{{- $sync := .Values.ntp.sync -}}
{{- if hasKey .Values.ftl "ntp_sync_active" -}}
{{- $sync = index .Values.ftl "ntp_sync_active" -}}
{{- else if hasKey .Values.extraEnvVars "FTLCONF_ntp_sync_active" -}}
{{- $sync = index .Values.extraEnvVars "FTLCONF_ntp_sync_active" -}}
{{- end -}}
{{- if eq (toString $sync | lower) "true" -}}
true
{{- end -}}
{{- end }}

{{/*
Capabilities of the Pi-hole container: the given capabilities map plus SYS_TIME, which the NTP
client needs to set the clock. Call with (dict "root" $ "capabilities" <map> "privileged" <value>).
Nothing is added when the container is privileged or SYS_TIME is already listed.
*/}}
{{- define "pihole.capabilities" -}}
{{- $caps := deepCopy (.capabilities | default dict) -}}
{{- if and (include "pihole.ntpSync" .root) (ne (toString .privileged) "true") -}}
{{- $add := $caps.add | default list -}}
{{- if not (has "SYS_TIME" $add) -}}
{{- $_ := set $caps "add" (append $add "SYS_TIME") -}}
{{- end -}}
{{- end -}}
{{- with $caps -}}
{{- toYaml . -}}
{{- end -}}
{{- end }}
