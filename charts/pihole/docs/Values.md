# Values

## admin

### admin.annotations

By allowing annotations to be added to the password secret, we can use tools like [Reflector](https://github.com/emberstack/kubernetes-reflector) to synchronize secrets across namespaces. 

This is interesting e.g. with the [ExternalDNS](https://github.com/kubernetes-sigs/external-dns) 0.14+'s Pi-Hole integration that can automatically expose Ingress host names to the Local DNS configuration:

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: external-dns
spec:
  strategy:
    type: Recreate
  selector:
    matchLabels:
      app: external-dns
  template:
    metadata:
      labels:
        app: external-dns
    spec:
      serviceAccountName: external-dns
      containers:
      - name: external-dns
        image: registry.k8s.io/external-dns/external-dns:v0.14.0
        # If authentication is disabled and/or you didn't create
        # a secret, you can remove this block.
        envFrom:
          - secretRef:
              # Change this if you gave the secret a different name
              name: pihole-password
        args:
          - --source=service
          - --source=ingress
          # Pihole only supports A/CNAME records so there is no mechanism to track ownership.
          # You don't need to set this flag, but if you leave it unset, you will receive warning
          # logs when ExternalDNS attempts to create TXT records.
          - --registry=noop
          # IMPORTANT: If you have records that you manage manually in Pi-hole, set
          # the policy to upsert-only so they do not get deleted.
          - --policy=upsert-only
          - --provider=pihole
          # Change this to the actual address of your Pi-hole web server
          - --pihole-server=http://pihole-web.pihole.svc.cluster.local
        resources:
          limits:
            cpu: 1
            memory: 1Gi
          requests:
            cpu: 100m
            memory: 256M
      securityContext:
        fsGroup: 65534 # For ExternalDNS to be able to read Kubernetes token files
```

Since the Secret reference can only refer to a secret in the same namespace as ExternalDNS, using Reflector is a viable option to synchronize the two secrets. This can now be done via

```yaml
admin:
  enabled: true
  existingSecret: ""
  passwordKey: "password"
  annotations:
    reflector.v1.k8s.emberstack.com/reflection-allowed: "true"
    reflector.v1.k8s.emberstack.com/reflection-allowed-namespaces: "external-dns"
```

For Reflector to work we also need to create the mirror (target) secret in ExternalDNS' namespace like this:

```yaml
apiVersion: v1
kind: Secret
metadata:
  # Change this to match the secretRef used in the ExternalDNS deployment:
  name: pihole-password
  # Change this to ExternalDNS' namespace:
  namespace: external-dns
  annotations:
    # Change this to address the pihole password secret: 'namespace/secret-name':
    reflector.v1.k8s.emberstack.com/reflects: "pihole/pihole-password"
data: {}  # Will be overwritten by Reflector
```
