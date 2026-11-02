# Destek+ bağlantı sunucusu kurulumu

Destek+ cihazların birbirini ID ile bulması ve modem/NAT arkasından bağlanabilmesi için
küçük bir sunucuya ihtiyaç duyar. Sunucu sadece eşleştirme ve gerekirse trafik aktarımı
(relay) yapar. Ekran görüntüsü şifreli gider, sunucu içeriği göremez.

Sunucu kurulmadan da uygulama çalışır: bu durumda RustDesk'in ücretsiz genel sunucusu
kullanılır (bazen yavaş olabilir).

## 1. Sunucu kirala

Herhangi bir Linux VPS yeter (1 CPU, 1 GB RAM). Örnek: Hetzner, DigitalOcean, Contabo,
ya da Türkiye'deki bir sağlayıcı. Ubuntu 22.04/24.04 seç. Sabit bir IP adresin olacak
(örnek: `203.0.113.10`). İstersen bir alan adı da yönlendirebilirsin (örnek: `destek.medyado.tr`).

## 2. Portları aç

Sağlayıcının güvenlik duvarında ve sunucuda şu portları aç:

| Port | Protokol | Ne için |
|------|----------|---------|
| 21115 | TCP | NAT testi |
| 21116 | TCP + UDP | ID kaydı ve eşleştirme |
| 21117 | TCP | Relay (aktarma) |
| 21118, 21119 | TCP | Web istemcisi (isteğe bağlı) |

Ubuntu'da:

```bash
sudo ufw allow 21115:21117/tcp
sudo ufw allow 21116/udp
```

## 3. Docker ile kur

```bash
curl -fsSL https://get.docker.com | sudo sh
git clone https://github.com/metinnmercann/destek-plus.git
cd destek-plus/server
sudo docker compose up -d
```

## 4. Açık anahtarı al

Sunucu ilk açılışta bir anahtar üretir:

```bash
cat data/id_ed25519.pub
```

Çıkan satırı (ör. `AbCd...=`) kopyala. Bu anahtar sadece senin sunucuna bağlanan
uygulamaların bağlantıyı doğrulamasını sağlar. `data/id_ed25519` dosyasını (pub olmayan)
kimseyle paylaşma ve yedekle.

## 5. Uygulamaya göm

GitHub'da repo sayfası > **Settings > Secrets and variables > Actions > New repository secret**:

- `DESTEK_SERVER` = sunucunun IP adresi veya alan adı (ör. `destek.medyado.tr`)
- `DESTEK_KEY` = 4. adımda kopyaladığın anahtar

Sonra **Actions > Destek+ derleme > Run workflow** ile yeniden derle. Yeni kurulum
dosyaları otomatik olarak senin sunucunu kullanır, kullanıcının hiçbir ayar yapmasına
gerek kalmaz.

> İkisini birlikte ayarla. Sadece sunucuyu girip anahtarı boş bırakırsan bağlantılar
> "anahtar uyuşmuyor" hatası verir.

## Sorun giderme

- `sudo docker compose logs -f` ile kayıtları izle.
- Cihazlar "Hazır değil / bağlanılamıyor" diyorsa önce 21116 TCP ve UDP portlarının açık
  olduğunu kontrol et.
