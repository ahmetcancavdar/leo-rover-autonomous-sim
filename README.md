# Autonomous Leo Rover Simulation (ROS 2 Humble + Docker)

Bu proje, Ubuntu 22.04 üzerinde ROS 2 Humble kullanılarak geliştirilmiş, **Leo Rover** robotunun Gazebo simülasyon ortamında herhangi bir donanım veya yazılım kurmadan **sadece Docker üzerinden** otonom navigasyon (Go-To-Goal) yeteneğini sergilemektedir.

Araç, tekerlek kaymalarından (skid-steer) kaynaklı sapmaları engellemek için doğrudan simülasyonun Ground Truth Odometrisini (`/odom_true`) kullanarak milimetrik hata payıyla (`0.05m`) verilen X ve Y koordinatlarına kendi yönünü bularak ilerler.

## 🚀 Özellikler
1. **Sıfır Kurulum:** Tüm ROS 2 Humble, Gazebo, ve Python bağımlılıkları Dockerfile içerisine entegredir. Host bilgisayarınızda sadece Docker bulunması yeterlidir.
2. **X11 Forwarding:** Simülasyon arayüzleri, konteyner içerisinden doğrudan sizin bilgisayarınızın ekranına yansıtılır.
3. **Kusursuz Ground-Truth Odometri:** Tekerlek kaymalarında bile hedefini şaşırmaması için Gazebo Physics Engine'den doğrudan mutlak konum köprüsü kurulmuştur.
4. **Renklendirilmiş & Çizili Gazebo Haritası:** 
   - 🟦 **Mavi Kutu:** (0,0) Başlangıç noktası
   - 🟥 **Kırmızı Çizgi:** X Ekseni
   - 🟩 **Yeşil Çizgi:** Y Ekseni
   - ⬜ **Noktalar:** Her bir `1.0` metrelik / tam sayılı hücre kesişimleri
5. **Dinamik P-Controller:** `go_to_goal` ROS 2 Node'u yavaşlama ve eksen dönüş hızlarını pürüzsüz ayarlayan oransal hız kontrolcüsüne sahiptir.

---

## 🛠️ Kurulum & Çalıştırma Nasıl Yapılır?

Sisteminizin çalışması için her biri farklı görevler üstlenen **iki ayrı terminale** ihtiyacımız olacak.

### Adım 1: Ana Simülasyonu Başlatmak
Projeyi bilgisayarınıza klonladıktan sonra dizine gidin ve 1. Terminali açın:
```bash
git clone <sizin-repo-url-adresiniz>
cd antiotonom

# Konteyneri başlatın ve ekran iznini verin
./start_docker.sh
```
*(Eğer parolanız sorulursa girin. Ardından `root@leo_sim_container:/ros2_ws#` şeklinde Docker'ın içine erişeceksiniz)*

Docker içerisindeyken sistemi ayağa kaldırın:
```bash
source install/setup.bash
ros2 launch leo_nav_custom sim.launch.py
```
> Bu komuttan birkaç saniye sonra Gazebo 3D simülasyon haritası açılacak ve robotumuz `(0,0)` Mavi kutusunda belirecektir.

### Adım 2: Robota (X, Y) Hedefi Vermek
Gazebo ve navigasyon algoritması akarken ona dışarıdan hedef koordinat iletmek için yeni bir terminal açın (Host makinenizde) ve Docker'a girin:
```bash
docker exec -it leo_sim_container bash
```

Ardından hedef verici Python yazılımımızı çalıştırın:
```bash
source install/setup.bash
ros2 run leo_nav_custom user_input
```
**Ekranda çıkan soruya:**
- X Koordinatı: `2`
- Y Koordinatı: `-3` 
Gibi değerler girip Enter'a bastığınızda robot rotasını çevirip otonom olarak oraya gidecektir!

---

## 📁 Proje Yapısı

- `Dockerfile` & `docker-compose.yml`: Bağımlılıkları ve X11 bağlantılarını izole kurar.
- `start_docker.sh`: GUI görüntü aktarımına yetki verip, konteyneri interactive olarak çalıştırır.
- `ros2_ws/src/leo_simulator-ros2/`: Leo Rover'ın resmi fizik ve URDF eklentileri (Ground-truth odometri eklentisiyle modifiye edilmiş hali).
- `ros2_ws/src/leo_nav_custom/`: Sizin algoritmanızı ve haritanızı içeren özel paket.
  - `go_to_goal.py`: Koordinatlara gitmeyi sağlayan P-Controller.
  - `user_input.py`: Kullanıcıdan konsol üzerinden anlık X-Y değeri alan script.
  - `generate_grid.py`: Gazebo haritasındaki noktaları ve renkli eksenleri çizen jeneratör.

---
**Not:** Simülasyon donarsa veya yeniden başlatmak isterseniz Host terminalinden `docker restart leo_sim_container` yazıp Adım 1'i tekrarlamanız yeterlidir.
