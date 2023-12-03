# İHA Kiralama Projesi

Bu proje, Django framework kullanılarak geliştirilmiş bir İHA (İnsansız Hava Aracı) kiralama uygulamasını içermektedir.

## Başlangıç

Aşağıdaki adımları takip ederek projeyi yerel makinenizde çalıştırabilirsiniz.

### Önkoşullar

- Docker ve Docker Compose yüklü olmalıdır. [Docker İndirme Sayfası](https://www.docker.com/get-started)

### Kurulum

1. Projeyi klonlayın:

    ```bash
    git clone https://github.com/KULLANICI_ADINIZ/IHA-Kiralama-Projesi.git
    cd IHA-Kiralama-Projesi
    ```

2. Docker ile projeyi ayağa kaldırın:

    ```bash
    docker-compose up --build
    ```

    Bu komut, gerekli bağımlılıkları yükleyecek ve Django uygulamasını başlatacaktır.

3. Tarayıcıda aşağıdaki adresi ziyaret edin:

    ```
    http://localhost:8000
    ```

    Django uygulamanızı bu adres üzerinden görebilirsiniz.

4. Django admin paneline erişim sağlamak için oluşturulan superuser bilgileri:

    - Kullanıcı Adı: admin
    - Şifre: admin123 (veya seçtiğiniz şifre)

## Kullanım

Proje başlatıldıktan sonra, İHA Kiralama uygulamanızı kullanabilir ve Django admin panelini yönetebilirsiniz.

## Katkıda Bulunma

Eğer projeye katkıda bulunmak istiyorsanız, lütfen bir çekme isteği (pull request) göndermeden önce geliştirme ortamınızda test ettiğinizden emin olun.

## Lisans

Bu proje MIT lisansı ile lisanslanmıştır. Detaylı bilgi için [LICENSE.md](LICENSE.md) dosyasına göz atabilirsiniz.
