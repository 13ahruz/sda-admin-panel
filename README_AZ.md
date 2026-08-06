# Admin Panel İstifadə Təlimatı

## Ümumi Məlumat

Bu admin panel SDA veb saytının bütün məzmununu idarə etmək üçün nəzərdə tutulmuşdur. Bütün məlumatlar üç dildə (İngilis, Azərbaycan və Rus) saxlanılır və veb saytda dinamik olaraq göstərilir.

---

## 📋 Məzmun Cədvəli

1. [Contact Messages (Əlaqə Mesajları)](#1-contact-messages)
2. [About Sections (Haqqımızda)](#2-about-sections)
3. [Partners (Partnyorlar)](#3-partners)
4. [Property Sectors (Əmlak Sektorları)](#4-property-sectors)
5. [Projects (Layihələr)](#5-projects)
6. [Services (Xidmətlər)](#6-services)
7. [News Articles (Xəbərlər)](#7-news-articles)
8. [Team Members (Komanda Üzvləri)](#8-team-members)
9. [Approaches (Yanaşmalar)](#9-approaches)

---

## 1. Contact Messages (Əlaqə Mesajları)

**İstifadə olunduğu səhifələr:** Contact (Əlaqə), Careers (Karyera)

### Nə üçün istifadə olunur?
Saytdan gələn bütün əlaqə formalarını və iş müraciətlərini saxlayır. Müştərilər və namizədlər saytın "Contact" və "Careers" bölmələrindən mesaj göndərdikdə burada görünür.

### Sahələr:

| Sahə | Açıqlama | Məcburi |
|------|----------|---------|
| **name** | Müştərinin tam adı (Contact forması üçün) | Bəli (Contact üçün) |
| **first_name** | Müştərinin adı (Careers forması üçün) | Bəli (Careers üçün) |
| **last_name** | Müştərinin soyadı (Careers forması üçün) | Bəli (Careers üçün) |
| **phone_number** | Telefon nömrəsi | Bəli |
| **email** | Email ünvanı | Bəli |
| **message** | Mesaj mətni | Xeyr |
| **company** | Şirkət adı (Contact forması üçün) | Xeyr |
| **country** | Ölkə (Contact forması üçün) | Xeyr |
| **property_type** | Əmlak tipi (Contact forması üçün) | Xeyr |
| **cv_url** | CV faylının linki (Careers forması üçün) | Xeyr |
| **is_read** | Oxunub/oxunmayıb statusu | Avtomatik |
| **status** | Mesajın statusu (new, in_progress, completed) | Avtomatik |
| **created_at** | Yaranma tarixi | Avtomatik |

### Necə istifadə edilir?
- Müştərilər Contact səhifəsindən mesaj göndərdikdə name, email, phone, company, country, property_type doldurulur
- Karyera müraciətləri olduqda first_name, last_name, email, phone, cv_url doldurulur
- Admin paneldə mesajları oxuya və statusunu dəyişə bilərsiniz
- Mesajları oxunmuş kimi qeyd etmək üçün "is_read" checkbox-u işarələyin

---

## 2. About Sections (Haqqımızda Bölməsi)

**İstifadə olunduğu səhifələr:** Ana səhifə (Home page)

### Nə üçün istifadə olunur?
Ana səhifədəki statistika bölməsində göstərilən rəqəmləri saxlayır (təcrübə illəri, davam edən layihələr, komanda üzvləri).

### Sahələr:

| Sahə | Açıqlama | Məcburi |
|------|----------|---------|
| **years_experience** | İş təcrübəsi (il) | Bəli |
| **ongoing_projects** | Davam edən layihələrin sayı | Bəli |
| **team_members** | Komanda üzvlərinin sayı | Bəli |

### Necə istifadə edilir?
- Adətən yalnız 1 qeyd olmalıdır
- Ana səhifədə "Years of Experience", "Ongoing Projects", "Team Members" rəqəmləri kimi göstərilir
- Rəqəmləri düzəliş etmək üçün mövcud qeydi redaktə edin

### Nümunə:
```
Years Experience: 15
Ongoing Projects: 45
Team Members: 20
```

---

## 3. Partners (Partnyorlar)

**İstifadə olunduğu səhifələr:** Ana səhifə (Home page - Partners bölməsi)

### Nə üçün istifadə olunur?
Şirkətin əməkdaşlıq etdiyi partnyorların loqolarını göstərir.

### Sahələr:

#### Partner (Əsas qeyd):
| Sahə | Açıqlama | Məcburi |
|------|----------|---------|
| **title** | Partnyor adı | Xeyr |

#### Partner Logo (Alt qeydlər):
| Sahə | Açıqlama | Məcburi |
|------|----------|---------|
| **partner** | Hansı partnyor aid olduğu | Bəli |
| **image_url** | Loqo şəkli | Bəli |
| **order** | Göstərilmə sırası | Bəli |

### Necə istifadə edilir?
1. Yeni partnyor əlavə edin (məsələn, "Technology Partners")
2. Partner məlumatlarına daxil olun
3. "Partner Logos" bölməsindən loqo şəkilləri əlavə edin
4. Order sahəsi ilə sıralamada dəyişiklik edə bilərsiniz

### Qeyd:
- Bir partnyor altında bir neçə loqo ola bilər
- Loqolar ana səhifədə karusel şəklində göstərilir

---

## 4. Property Sectors (Əmlak Sektorları)

**İstifadə olunduğu səhifələr:** Ana səhifə (Services bölməsi), Property Sectors səhifəsi

### Nə üçün istifadə olunur?
Şirkətin təklif etdiyi əmlak sektorlarını (məsələn, ticarət, yaşayış, sənaye) göstərir və hər sektora aid xidmətləri təsvir edir.

### Sahələr:

#### Property Sector (Əsas qeyd):
| Sahə | Açıqlama | Məcburi |
|------|----------|---------|
| **title_en / title_az / title_ru** | Sektor adı (3 dildə) | Bəli |
| **description_en / description_az / description_ru** | Sektor təsviri (3 dildə) | Bəli |
| **featured_project_1** | Seçilmiş layihə 1 | Xeyr |
| **featured_project_2** | Seçilmiş layihə 2 | Xeyr |
| **featured_project_3** | Seçilmiş layihə 3 | Xeyr |
| **order** | Göstərilmə sırası | Bəli |

#### Property Sectors Services (Alt qeydlər):
| Sahə | Açıqlama | Məcburi |
|------|----------|---------|
| **property_sector** | Hansı sektora aid olduğu | Bəli |
| **title_en / title_az / title_ru** | Xidmət adı (3 dildə) | Bəli |
| **description_en / description_az / description_ru** | Xidmət təsviri (3 dildə) | Bəli |
| **order** | Göstərilmə sırası | Bəli |

### Necə istifadə edilir?
1. Yeni sektor əlavə edin (məsələn, "Commercial Real Estate")
2. Üç dildə başlıq və təsvir yazın
3. Featured projects bölməsindən ən yaxşı layihələri seçin
4. "Property Sectors Services" bölməsindən xidmətləri əlavə edin

### Nümunə:
```
Title (EN): Commercial Real Estate
Title (AZ): Kommersiya Əmlakı
Description: Ticarət mərkəzləri, ofis binaları və s.
Featured Projects: Mall Project, Office Complex
Services: Property Management, Leasing, Valuation
```

---

## 5. Projects (Layihələr)

**İstifadə olunduğu səhifələr:** Ana səhifə, Projects səhifəsi, Project Detail səhifəsi, Service Detail səhifəsi

### Nə üçün istifadə olunur?
Şirkətin həyata keçirdiyi bütün layihələrin portfeyini göstərir.

### Sahələr:

#### Project (Əsas qeyd):
| Sahə | Açıqlama | Məcburi |
|------|----------|---------|
| **title_en / title_az / title_ru** | Layihə adı (3 dildə) | Bəli |
| **description_en / description_az / description_ru** | Qısa təsvir (3 dildə) | Bəli |
| **about_project_en / about_project_az / about_project_ru** | Ətraflı təsvir (3 dildə) | Xeyr |
| **slug** | URL-də istifadə edilən unikal ad | Bəli |
| **tag** | Layihə etiketi (məsələn, "Completed") | Xeyr |
| **client** | Müştəri adı | Xeyr |
| **year** | Layihənin ili | Xeyr |
| **property_sector** | Hansı sektora aid olduğu | Xeyr |
| **cover_photo_url** | Əsas şəkil | Xeyr |
| **services** | Layihədə istifadə edilən xidmətlər | Xeyr |

#### Project Delivered Solutions (Alt qeydlər):
| Sahə | Açıqlama | Məcburi |
|------|----------|---------|
| **project** | Hansı layihəyə aid olduğu | Bəli |
| **title_en / title_az / title_ru** | Həll adı (3 dildə) | Bəli |
| **description_en / description_az / description_ru** | Həll təsviri (3 dildə) | Bəli |
| **order** | Göstərilmə sırası | Bəli |

#### Project Photos (Alt qeydlər):
| Sahə | Açıqlama | Məcburi |
|------|----------|---------|
| **project** | Hansı layihəyə aid olduğu | Bəli |
| **image_url** | Şəkil linki | Bəli |
| **order** | Göstərilmə sırası | Bəli |

### Necə istifadə edilir?
1. Yeni layihə əlavə edin
2. Üç dildə məlumatları doldurun
3. Slug avtomatik yaranır, amma dəyişdirə bilərsiniz (URL üçün)
4. Property Sector və Services seçin
5. "Project Delivered Solutions" bölməsindən layihənin təqdim etdiyi həlləri yazın
6. "Project Photos" bölməsindən qalereya şəkilləri əlavə edin

### Slug nümunəsi:
- Title: "Baku Mall Project" → Slug: "baku-mall-project"
- URL: website.com/projects/baku-mall-project

---

## 6. Services (Xidmətlər)

**İstifadə olunduğu səhifələr:** Ana səhifə, Services səhifəsi, Service Detail səhifəsi

### Nə üçün istifadə olunur?
Şirkətin təklif etdiyi xidmətləri və onların detallarını göstərir.

### Sahələr:

#### Service (Əsas qeyd):
| Sahə | Açıqlama | Məcburi |
|------|----------|---------|
| **name_en / name_az / name_ru** | Xidmət adı (3 dildə) | Bəli |
| **description_en / description_az / description_ru** | Qısa təsvir (3 dildə) | Bəli |
| **hero_text_en / hero_text_az / hero_text_ru** | Hero bölməsində göstərilən mətn | Xeyr |
| **meta_title_en / meta_title_az / meta_ru** | SEO başlığı | Xeyr |
| **meta_description_en / meta_az / meta_ru** | SEO təsviri | Xeyr |
| **slug** | URL-də istifadə edilən unikal ad | Bəli |
| **image_url** | Xidmət şəkli | Xeyr |
| **order** | Göstərilmə sırası | Bəli |
| **featured_project_1** | Seçilmiş layihə 1 | Xeyr |
| **featured_project_2** | Seçilmiş layihə 2 | Xeyr |

#### Service Benefits (Alt qeydlər):
| Sahə | Açıqlama | Məcburi |
|------|----------|---------|
| **service** | Hansı xidmətə aid olduğu | Bəli |
| **title_en / title_az / title_ru** | Fayda başlığı (3 dildə) | Bəli |
| **description_en / description_az / description_ru** | Fayda təsviri (3 dildə) | Bəli |
| **order** | Göstərilmə sırası | Bəli |

#### Service What We Do Items (Alt qeydlər):
| Sahə | Açıqlama | Məcburi |
|------|----------|---------|
| **service** | Hansı xidmətə aid olduğu | Bəli |
| **title_en / title_az / title_ru** | Əməliyyat adı (3 dildə) | Bəli |
| **description_en / description_az / description_ru** | Əməliyyat təsviri (3 dildə) | Bəli |
| **icon_url** | İkon şəkli | Xeyr |
| **order** | Göstərilmə sırası | Bəli |

#### Service Process Steps (Alt qeydlər):
| Sahə | Açıqlama | Məcburi |
|------|----------|---------|
| **service** | Hansı xidmətə aid olduğu | Bəli |
| **title_en / title_az / title_ru** | Proses addımı (3 dildə) | Bəli |
| **description_en / description_az / description_ru** | Addım təsviri (3 dildə) | Bəli |
| **order** | Göstərilmə sırası | Bəli |

### Necə istifadə edilir?
1. Yeni xidmət əlavə edin (məsələn, "Property Management")
2. Üç dildə məlumatları doldurun
3. Image_url sahəsinə şəkil yükləyin (Service detail səhifəsində göstərilir)
4. "Service Benefits" - xidmətin faydalarını yazın
5. "Service What We Do Items" - bu xidmət çərçivəsində nələr etdiyinizi yazın (ikonla)
6. "Service Process Steps" - iş prosesinin addımlarını yazın (nömrələnmiş)

### Fərq:
- **What We Do Items**: İkonlu göstərilir, xidmətin əsas komponentləri
- **Process Steps**: Nömrələnmiş addımlar, xidmətin iş axını

---

## 7. News Articles (Xəbərlər)

**İstifadə olunduğu səhifələr:** Ana səhifə, News səhifəsi, News Detail səhifəsi

### Nə üçün istifadə olunur?
Şirkət xəbərləri, bloq yazıları və elanlar üçün istifadə olunur.

### Sahələr:

#### News Article (Əsas qeyd):
| Sahə | Açıqlama | Məcburi |
|------|----------|---------|
| **title_en / title_az / title_ru** | Xəbər başlığı (3 dildə) | Bəli |
| **summary_en / summary_az / summary_ru** | Qısa xülasə (3 dildə) | Xeyr |
| **photo_url** | Əsas şəkil | Xeyr |
| **tag_en / tag_az / tag_ru** | Xəbər kateqoriyası (3 dildə) | Xeyr |
| **tags** | Etiketlər siyahısı | Xeyr |

#### News Sections (Alt qeydlər):
| Sahə | Açıqlama | Məcburi |
|------|----------|---------|
| **news** | Hansı xəbərə aid olduğu | Bəli |
| **heading_en / heading_az / heading_ru** | Bölmə başlığı (3 dildə) | Xeyr |
| **content_en / content_az / content_ru** | Bölmə məzmunu (3 dildə) | Xeyr |
| **image_url** | Bölmə şəkli | Xeyr |
| **order** | Göstərilmə sırası | Bəli |

### Necə istifadə edilir?
1. Yeni xəbər əlavə edin
2. Üç dildə başlıq və xülasə yazın
3. Photo_url sahəsinə əsas şəkil yükləyin
4. Tag sahəsinə kateqoriya yazın (məsələn, "Company News", "Industry Insights")
5. "News Sections" bölməsindən məqalə bölmələrini əlavə edin
6. Hər bölmə başlıq, mətn və şəkil ola bilər

### Struktur:
```
News Article
├── Title, Summary, Main Photo, Tag
└── News Sections
    ├── Section 1: Heading + Content + Image
    ├── Section 2: Heading + Content + Image
    └── Section 3: Heading + Content
```

---

## 8. Team Members (Komanda Üzvləri)

**İstifadə olunduğu səhifələr:** About Us səhifəsi, Team səhifəsi

### Nə üçün istifadə olunur?
Şirkət komanda üzvlərinin profilini göstərir.

### Sahələr:

| Sahə | Açıqlama | Məcburi |
|------|----------|---------|
| **full_name_en / full_name_az / full_name_ru** | Tam ad (3 dildə) | Bəli |
| **role_en / role_az / role_ru** | Vəzifə (3 dildə) | Bəli |
| **bio_en / bio_az / bio_ru** | Bioqrafiya (3 dildə) | Xeyr |
| **photo_url** | Profil şəkli | Xeyr |
| **linkedin_url** | LinkedIn profil linki | Xeyr |

### Necə istifadə edilir?
1. Yeni komanda üzvü əlavə edin
2. Üç dildə ad, vəzifə və bioqrafiya yazın
3. Photo_url sahəsinə profil şəkli yükləyin
4. LinkedIn_url sahəsinə LinkedIn profil linkini əlavə edin

### Nümunə:
```
Full Name (EN): John Smith
Full Name (AZ): Con Smit
Role (EN): CEO & Founder
Role (AZ): İcraçı Direktor və Təsisçi
Bio: 15+ years of experience in real estate...
LinkedIn: https://linkedin.com/in/johnsmith
```

---

## 9. Approaches (Yanaşmalar)

**İstifadə olunduğu səhifələr:** About Us səhifəsi

### Nə üçün istifadə olunur?
Şirkətin iş prinsiplərini və yanaşmasını göstərir.

### Sahələr:

| Sahə | Açıqlama | Məcburi |
|------|----------|---------|
| **title_en / title_az / title_ru** | Yanaşma başlığı (3 dildə) | Bəli |
| **description_en / description_az / description_ru** | Yanaşma təsviri (3 dildə) | Bəli |
| **order** | Göstərilmə sırası | Bəli |

### Necə istifadə edilir?
1. Yeni yanaşma əlavə edin (məsələn, "Client-Focused", "Innovation-Driven")
2. Üç dildə başlıq və təsvir yazın
3. Order sahəsi ilə sıralamada dəyişiklik edin

### Nümunə:
```
Title (EN): Client-Focused Approach
Title (AZ): Müştəri Yönümlü Yanaşma
Description: We prioritize our clients' needs...
Order: 1
```

---

## 🎨 Şəkil Yükləmə Qaydaları

### Şəkil Yükləmək Üçün:
1. Admin paneldə müvafiq sahəni tapın (məsələn, image_url, photo_url)
2. "Choose File" düyməsinə klikləyin
3. Kompüterinizdən şəkil seçin
4. Şəkil avtomatik yüklənəcək və link yaranacaq

### Tövsiyələr:
- **Format**: JPG, PNG və WebP formatları qəbul edilir
- **Ölçü**: Maksimum 5MB
- **Keyfiyyət**: Yüksək keyfiyyətli şəkillər istifadə edin
- **Nisbət**: Hər sahə üçün tövsiyə olunan nisbətlər:
  - Cover photos: 16:9 (məsələn, 1920x1080)
  - Team photos: 1:1 (məsələn, 500x500)
  - Logos: PNG (şəffaf fon)

---

## 📝 Multilinqual (Çoxdilli) Sistemin İzahı

### Nə üçün 3 dil?
Sayt 3 dildə işləyir: İngilis (EN), Azərbaycan (AZ), Rus (RU)

### Necə doldurmalı?
Hər sahənin 3 versiyası var:
- `title_en` - İngilis dili
- `title_az` - Azərbaycan dili  
- `title_ru` - Rus dili

### Vacib:
- **Üç dildə də eyni məzmunu yazın** (tərcümə edilmiş)
- Boş buraxsanız, o dildə məlumat göstərilməyəcək
- Legacy sahələr (title, description) köhnə uyğunluq üçündür

### Nümunə:
```
name_en: Property Management
name_az: Əmlak İdarəetməsi
name_ru: Управление Недвижимостью
```

---

## 🔢 Order (Sıralama) Sahəsi

### Nə üçün istifadə olunur?
Elementlərin saytda göstərilmə sırasını təyin edir.

### Necə işləyir?
- Kiçik rəqəm = Əvvəl göstərilir
- Böyük rəqəm = Sonra göstərilir
- Eyni rəqəmlər = Yaranma tarixinə görə

### Nümunə:
```
Service A - Order: 1  (Birinci göstəriləcək)
Service B - Order: 2  (İkinci göstəriləcək)
Service C - Order: 3  (Üçüncü göstəriləcək)
```

---

## 🔗 Əlaqəli Qeydlər

### Featured Projects (Seçilmiş Layihələr)
Services və Property Sectors bölmələrində featured project sahələri var. Bu layihələr həmin xidmət və ya sektorun səhifəsində xüsusi olaraq vurğulanır.

### Project Services (Layihə Xidmətləri)
Hər layihə bir neçə xidmətlə əlaqələndirilə bilər. Bu, layihənin hansı xidmətlərdən istifadə etdiyini göstərir.

### Property Sector Relations
Layihələr property sektorlara bağlanır, bu da layihələri kateqoriyalaşdırmağa kömək edir.

---

## ⚡ Tez-tez İstifadə Olunan Əməliyyatlar

### Yeni Xəbər Əlavə Etmək:
1. News Articles → Add News Article
2. Üç dildə başlıq və xülasə daxil edin
3. Şəkil yükləyin
4. Save and continue editing
5. News Sections → Add another News Section
6. Bölmələri əlavə edin
7. Save

### Layihə Şəkilləri Əlavə Etmək:
1. Projects → Layihəni açın
2. Project Photos bölməsinə keçin
3. Add another Project Photo
4. Şəkil yükləyin, order təyin edin
5. Save

### Xidmət Prosesi Təyin Etmək:
1. Services → Xidməti açın
2. Service Process Steps bölməsinə keçin
3. Add another Service Process Step
4. Hər addımı əlavə edin (title, description, order)
5. Save

---

## 🚨 Diqqət Edilməli Məqamlar

### ⚠️ Slug Sahələri
- Slug unikaldır, təkrarlana bilməz
- Yalnız kiçik hərflər, rəqəmlər və tire (-) istifadə edin
- Boşluq və xüsusi simvollardan çəkinin
- Avtomatik yaranır, amma manual dəyişdirə bilərsiniz

### ⚠️ Şəkil Linkləri
- Şəkillər `/uploads/` qovluğunda saxlanılır
- Sistemdən silməzdən əvvəl admin paneldə silin
- Böyük şəkilləri yükləmədən əvvəl optimallaşdırın

### ⚠️ Order Sahələri
- Eyni order dəyərləri qarışıqlıq yarada bilər
- Unique rəqəmlər istifadə edin (1, 2, 3, 4...)
- Sonradan sıralamada dəyişiklik etmək asandır

### ⚠️ Multilinqual Məlumatlar
- Bütün üç dili doldurmağı unutmayın
- Tərcümələrin düzgünlüyünü yoxlayın
- Bir dildə boş buraxsanız, həmin dildə saytda göstərilməyəcək

---

## 📞 Texniki Dəstək

Admin panel ilə bağlı problemləriniz olarsa:
1. Səhv mesajını ekran şəklində çəkin
2. Hansı əməliyyatı etdiyinizi qeyd edin
3. Development komandasına məlumat verin

---

## 📚 Əlavə Qeydlər

### Managed = False
Bütün modellər `managed=False` parametri ilə təyin olunub. Bu o deməkdir ki, Django bu cədvəlləri yaratmır, yalnız mövcud cədvəlləri oxuyur. Əsas məlumat bazası FastAPI tərəfindən idarə olunur.

### Timestamps
Bütün qeydlərdə `created_at` və `updated_at` sahələri avtomatik doldurulur. Bunları manual dəyişdirməyə ehtiyac yoxdur.

### İstifadə Olunmayan Modellər
TeamSection, TeamSectionItem, WorkProcess modelləri sistemdə mövcuddur, amma hazırda veb saytda istifadə olunmur. Bunları admin paneldə görmək mümkün deyil.

---

**Son yenilənmə: 26 Dekabr 2025**
