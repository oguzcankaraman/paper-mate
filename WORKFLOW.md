# 🎯 Git Kullanım Kılavuzu - Ekip Üyeleri İçin

## İlk Kurulum (Bir kere)

1. **Repository'i klonla:**
```bash
git clone https://github.com/YOUR_USERNAME/papermate.git
cd papermate
```git 
2. Kendine bir branch oluştur:

```bash
git checkout -b feature/ismin-konu
# Örnek: git checkout -b feature/ahmet-pdf-parser
```
## Günlük Çalışma Döngüsü
### 1. **Çalışmaya Başlamadan Önce**
```bash
# Ana branch'e geç
git checkout main

# En son değişiklikleri çek
git pull origin main

# Kendi branch'ine geç (veya yeni oluştur)
git checkout feature/ismin-konu
# Veya: git checkout -b feature/ismin-konu

# Main'deki değişiklikleri kendi branch'ine al
git merge main
```
### 2. **Kod Yazarken**
```bash
# Yazdığın kodu kaydet
git add .

# Commit yap (anlamlı mesaj yaz!)
git commit -m "feat: add pdf text extraction"

# GitHub'a yolla
git push origin feature/ismin-konu
```
**İlk push'ta şu hatayı alacaksın:**
```
fatal: The current branch has no upstream branch.
```
**Çözüm:** Git'in söylediği komutu çalıştır:

```bash
git push --set-upstream origin feature/ismin-konu
```
### 3. **Pull Request (PR) Açma**
1. GitHub'da repository'e git
2. Sarı bir banner göreceksin: "Your recently pushed branches: feature/ismin-konu"
3. **"Compare & pull request"** butonuna bas
4. PR formunu doldur:

    - Title: Ne yaptığını özetle
    - Description: Detaylı açıklama
    - Reviewers: Team lead'i seç (onu etiketle)


5. **"Create pull request"** bas

### 4. **Review Bekle**

- Team lead kodu inceleyecek
- Değişiklik isterse, düzeltip tekrar push yap (aynı branch'e)
- Approve olunca merge edilecek

### 5. **Merge Edildikten Sonra**
```bash
# Ana branch'e geç
git checkout main

# Yeni değişiklikleri çek
git pull origin main

# Eski branch'i sil (temizlik)
git branch -d feature/ismin-konu
```
# ⚠️ Sık Karşılaşılan Hatalar
## "Merge conflict" hatası
```bash
# Main'den son değişiklikleri al
git checkout main
git pull origin main

# Kendi branch'ine geç
git checkout feature/ismin-konu

# Merge et
git merge main

# Eğer conflict varsa:
# 1. VS Code'da conflict'li dosyaları aç
# 2. "Accept Current Change" veya "Accept Incoming Change" seç
# 3. Kaydet
# 4. Commit yap:
git add .
git commit -m "fix: resolve merge conflicts"
git push
```
## "Permission denied" hatası
GitHub'a SSH key eklemedin. Team lead'e sor!
### "fatal: not a git repository"
Yanlış klasördesin. `cd paper-mate` ile doğru klasöre git.
#
💡 İpuçları

- Her gün çalışmaya başlamadan `git pull origin main` yap
- Küçük, sık commit'ler yap (günde 2-3 commit)
- Commit mesajlarını Türkçe yazabilirsin ama İngilizce daha profesyonel
- Takıldığın yerde Discord'dan sor!


