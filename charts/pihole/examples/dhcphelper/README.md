# Pi-hole with DHCP Helper

This example shows how to deploy Pi-hole with DHCP functionality **without** using `hostNetwork: true` on the Pi-hole pod. Instead, a lightweight DHCP helper container handles the Layer 2 broadcast requirements.

## Problem

DHCP operates at OSI Layer 2 using broadcast messages. In Kubernetes, pods typically cannot receive Layer 2 broadcasts because they are isolated in their own network namespace. The common workaround is to use `hostNetwork: true`, but this can cause issues:

- **Port conflicts**: If any port required by Pi-hole FTL (e.g., UDP port 53, 67, or others) is already in use on the host, FTL will fail to start with the error `pihole-FTL: no process found`
- **Security**: Host networking reduces container isolation
- **Flexibility**: Only one pod can use a specific port on a node

## Solution

Use a DHCP relay/helper that:
1. Runs with `hostNetwork: true` to receive DHCP broadcasts
2. Forwards DHCP requests as unicast to the Pi-hole pod
3. Relays DHCP responses back to clients as broadcasts

This approach keeps Pi-hole in normal pod networking while only the minimal DHCP helper needs host access.

## Architecture

```
┌─────────────────┐     DHCP Broadcast      ┌──────────────────┐
│  DHCP Client    │ ───────────────────────►│  DHCP Helper     │
│  (Layer 2)      │                         │  (hostNetwork)   │
└─────────────────┘                         └────────┬─────────┘
                                                     │ Unicast
                                                     ▼
                                            ┌──────────────────┐
                                            │  Pi-hole Pod     │
                                            │  (ClusterIP)     │
                                            └──────────────────┘
```

## Deployment

### 1. Deploy Pi-hole

Deploy Pi-hole using the provided values file. Pi-hole runs with normal pod networking and exposes DHCP via a ClusterIP service:

```bash
helm install pihole mojo2600/pihole -f pihole-values.yaml
```

**Important**: Note the ClusterIP assigned to the DHCP service after deployment:

```bash
kubectl get svc pihole-dhcp -o jsonpath='{.spec.clusterIP}'
```

### 2. Deploy DHCP Helper

Update the `PIHOLE_IP` in `dhcphelper.yaml` with the Pi-hole DHCP service ClusterIP, then deploy:

```bash
kubectl apply -f dhcphelper.yaml
```

## Configuration

### Pi-hole Values (`pihole-values.yaml`)

Key settings:
- `hostNetwork: false` - Pi-hole uses normal pod networking
- `serviceDhcp.enabled: true` - Exposes DHCP on a ClusterIP service
- `extraEnvVars.DHCP_ACTIVE: true` - Enables DHCP server in Pi-hole
- Adjust `DHCP_START`, `DHCP_END`, `DHCP_ROUTER` for your network

### DHCP Helper (`dhcphelper.yaml`)

Key settings:
- `hostNetwork: true` - Required to receive Layer 2 broadcasts
- `IP` environment variable - Must point to Pi-hole's DHCP service ClusterIP
- Runs on a specific node via `nodeSelector` (adjust for your cluster)

## Troubleshooting

### DHCP clients not receiving addresses

1. Verify the DHCP helper is running:
   ```bash
   kubectl get pods -l app=dhcphelper
   ```

2. Check the helper can reach Pi-hole:
   ```bash
   kubectl exec -it <dhcphelper-pod> -- nc -uzvw3 <pihole-ip> 67
   ```

3. Verify Pi-hole DHCP is enabled:
   - Access Pi-hole admin UI
   - Go to Settings → DHCP
   - Ensure DHCP server is enabled

### Multiple nodes

If you have multiple nodes and want DHCP on all of them, you can change the DHCP helper to a DaemonSet. Each node will then have its own helper forwarding to Pi-hole.

## References

- [homeall/dhcphelper](https://github.com/homeall/dhcphelper) - The DHCP helper container image
- [Pi-hole Docker DHCP documentation](https://github.com/pi-hole/docker-pi-hole#running-dhcp-from-docker-pi-hole)
