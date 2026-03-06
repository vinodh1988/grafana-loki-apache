# Docker Installation and Usage on Red Hat 9

This guide explains how to install Docker Engine on Red Hat Enterprise Linux 9 (RHEL 9) and run this project with Docker Compose.

## 1. Prerequisites

- RHEL 9 with `sudo` access
- Internet access
- System registered with Red Hat subscription (for required packages)

## 2. Remove old/conflicting container packages (optional but recommended)

```bash
sudo dnf remove -y podman buildah docker docker-client docker-common docker-engine
```

If you use Podman for other workloads, skip this step.

## 3. Install required utilities

```bash
sudo dnf install -y dnf-plugins-core device-mapper-persistent-data lvm2
```

## 4. Add Docker CE repository

```bash
sudo dnf config-manager --add-repo https://download.docker.com/linux/centos/docker-ce.repo
```

Note: Docker provides CentOS repo metadata that is commonly used on RHEL.

## 5. Install Docker Engine and Compose plugin

```bash
sudo dnf install -y docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin
```

## 6. Start and enable Docker service

```bash
sudo systemctl enable --now docker
sudo systemctl status docker --no-pager
```

## 7. Verify installation

```bash
docker --version
docker compose version
sudo docker run --rm hello-world
```

## 8. (Optional) Run Docker without sudo

```bash
sudo groupadd docker 2>/dev/null || true
sudo usermod -aG docker $USER
newgrp docker
```

Then verify:

```bash
docker ps
```

## 9. Run this project with Docker Compose

From the project directory:

```bash
cd apache-project
docker compose pull
docker compose up -d
```

Check running services:

```bash
docker compose ps
```

View logs:

```bash
docker compose logs -f
```

Stop services:

```bash
docker compose down
```

## 10. Open key endpoints

- App: `http://<server-ip>:8088/`
- Apache Exporter metrics: `http://<server-ip>:9117/metrics`
- Loki (API): `http://<server-ip>:3100/`

## 11. Firewall notes (if remote access is needed)

```bash
sudo firewall-cmd --permanent --add-port=8088/tcp
sudo firewall-cmd --permanent --add-port=9117/tcp
sudo firewall-cmd --permanent --add-port=3100/tcp
sudo firewall-cmd --reload
```

## 12. SELinux note

If SELinux is enforcing and you encounter permission issues on mounted volumes:

- Prefer adjusting volume labels/contexts (`:Z`/`:z`) in compose mounts when appropriate.
- Avoid disabling SELinux globally unless absolutely necessary.

## 13. Troubleshooting quick checks

```bash
systemctl is-active docker
journalctl -u docker --no-pager -n 100
docker info
```

If Docker packages fail to resolve:

- Confirm subscription status: `sudo subscription-manager status`
- Rebuild metadata: `sudo dnf clean all && sudo dnf makecache`
- Retry install command from step 5

If Apache exporter image fails with `failed to resolve reference`:

```bash
docker pull bitnami/apache-exporter:latest
docker compose pull apache-exporter
docker compose up -d apache-exporter
```

If your server cannot reach Docker Hub, use a registry mirror in `/etc/docker/daemon.json` and restart Docker:

```json
{
	"registry-mirrors": ["https://mirror.gcr.io"]
}
```

```bash
sudo systemctl restart docker
docker compose pull
```
