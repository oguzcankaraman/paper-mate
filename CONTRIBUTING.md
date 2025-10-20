# Contribution Guidelines

## Git Workflow

### 1. Branch Oluşturma
```bash
git checkout main
git checkout main
git checkout -b feature/team-X-feature-name
```

### Branch isimlendirme
- `feature/team1-pdf-parser` - yeni özellik
- `fix/team2-llm-error` - bug fix
- `docs/readme-update` - dokümantasyon

### 2. Değişiklik Yapma

```bash
# Dosyaları düzenle
# Test et!

git add .
git commit -m "feat: add pdf parser basic functionality"
```

### Commit Mesajı Formatı

- `feat:` - yeni özellik
- `fix:` - bug fix
- `docs:` - dökümantasyon
- `test:`- test ekleme
- `refactor:` - kod iyileştirme

### 3. Push ve Pull Request
```bash
git push origin feature/team-X-feature-name
```
GitHub'da PR aç (aşağıda detaylı anlatılacak)

### Code Quality
- Her fonksiyon için docstring yaz
- Test yaz (en az unit test)
- Black ile format et: `black .`
- Flake8 ile kontrol et: `flake8 src/`

### Review Process
- En az 1 kişinin approval'ı gerekli
- Tüm conversation'lar resolve olmalı
- CI testleri geçmeli (eklenince)