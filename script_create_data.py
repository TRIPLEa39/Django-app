import random
import requests
from io import BytesIO
from PIL import Image
import uuid
from datetime import timedelta
from django.utils import timezone
from django.contrib.auth.models import User
from blog.models import Post
from users.models import Profile

# Multilingual post data
POSTS_DATA = [
    # English
    {
        "title": "Learning Django Framework",
        "content": "Django is a powerful web framework for building scalable web applications. Today I learned about models, views, and templates which are the core components of Django MVC architecture.",
        "language": "English"
    },
    {
        "title": "Python Best Practices",
        "content": "Writing clean and maintainable Python code is essential. Always follow PEP 8 style guide, use meaningful variable names, and write comprehensive docstrings for your functions.",
        "language": "English"
    },
    {
        "title": "Web Development Tips",
        "content": "When building web applications, always prioritize security, performance, and user experience. Use proper authentication, optimize database queries, and ensure responsive design.",
        "language": "English"
    },
    
    # Spanish
    {
        "title": "Desarrollo Web con Django",
        "content": "Django es un framework muy poderoso para desarrollar aplicaciones web escalables. Hoy aprendí sobre modelos, vistas y plantillas que son los componentes principales de la arquitectura MVC de Django.",
        "language": "Spanish"
    },
    {
        "title": "Mejores Prácticas en Python",
        "content": "Escribir código Python limpio y mantenible es esencial. Siempre sigue la guía de estilo PEP 8, usa nombres de variables significativos y escribe docstrings comprensivos para tus funciones.",
        "language": "Spanish"
    },
    {
        "title": "Consejos de Desarrollo Web",
        "content": "Al construir aplicaciones web, siempre prioriza la seguridad, el rendimiento y la experiencia del usuario. Utiliza autenticación adecuada, optimiza consultas de base de datos y asegura un diseño responsive.",
        "language": "Spanish"
    },
    
    # German
    {
        "title": "Django Framework Lernen",
        "content": "Django ist ein leistungsstarkes Web-Framework zum Aufbau skalierbarer Webanwendungen. Heute habe ich etwas über Modelle, Ansichten und Vorlagen gelernt, die Kernkomponenten der Django MVC-Architektur sind.",
        "language": "German"
    },
    {
        "title": "Python Best Practices",
        "content": "Das Schreiben von sauberem und wartbarem Python-Code ist essentiell. Befolgen Sie immer den PEP 8-Stilführer, verwenden Sie aussagekräftige Variablennamen und schreiben Sie umfassende Dokumentationen für Ihre Funktionen.",
        "language": "German"
    },
    {
        "title": "Webentwicklungs-Tipps",
        "content": "Bei der Erstellung von Webanwendungen sollten Sie immer Sicherheit, Leistung und Benutzererfahrung priorisieren. Verwenden Sie ordnungsgemäße Authentifizierung, optimieren Sie Datenbankabfragen und sorgen Sie für responsives Design.",
        "language": "German"
    },
    
    # French
    {
        "title": "Apprentissage du Framework Django",
        "content": "Django est un framework web puissant pour la construction d'applications web évolutives. Aujourd'hui, j'ai appris les modèles, les vues et les templates qui sont les composants principaux de l'architecture MVC de Django.",
        "language": "French"
    },
    {
        "title": "Bonnes Pratiques Python",
        "content": "Écrire du code Python propre et maintenable est essentiel. Suivez toujours le guide de style PEP 8, utilisez des noms de variables significatifs et écrivez des docstrings complètes pour vos fonctions.",
        "language": "French"
    },
    
    # Arabic
    {
        "title": "تعلم إطار عمل Django",
        "content": "Django هو إطار عمل ويب قوي لبناء تطبيقات ويب قابلة للتوسع. تعلمت اليوم عن النماذج والعروض والقوالب وهي المكونات الأساسية لهندسة Django MVC.",
        "language": "Arabic"
    },
    {
        "title": "أفضل الممارسات في Python",
        "content": "كتابة كود Python نظيف وسهل الصيانة أمر ضروري. اتبع دائماً دليل أسلوب PEP 8 واستخدم أسماء متغيرات ذات معنى واكتب سلاسل توثيق شاملة لوظائفك.",
        "language": "Arabic"
    },
    
    # Italian
    {
        "title": "Imparare il Framework Django",
        "content": "Django è un framework web potente per la creazione di applicazioni web scalabili. Oggi ho imparato i modelli, le visualizzazioni e i template che sono i componenti principali dell'architettura MVC di Django.",
        "language": "Italian"
    },
    {
        "title": "Migliori Pratiche in Python",
        "content": "Scrivere codice Python pulito e mantenibile è essenziale. Seguire sempre la guida di stile PEP 8, utilizzare nomi di variabili significativi e scrivere docstring completi per le tue funzioni.",
        "language": "Italian"
    },
    
    # Portuguese
    {
        "title": "Aprendendo Django Framework",
        "content": "Django é um framework web poderoso para construir aplicações web escaláveis. Hoje aprendi sobre modelos, visualizações e templates que são os componentes principais da arquitetura MVC do Django.",
        "language": "Portuguese"
    },
    {
        "title": "Melhores Práticas em Python",
        "content": "Escrever código Python limpo e fácil de manter é essencial. Sempre siga o guia de estilo PEP 8, use nomes de variáveis significativos e escreva docstrings abrangentes para suas funções.",
        "language": "Portuguese"
    },
    
    # Japanese
    {
        "title": "Djangoフレームワークを学ぶ",
        "content": "Djangoはスケーラブルなウェブアプリケーションを構築するための強力なウェブフレームワークです。今日、Djangoの根本的なコンポーネントであるモデル、ビュー、テンプレートについて学びました。",
        "language": "Japanese"
    },
    {
        "title": "Pythonのベストプラクティス",
        "content": "クリーンで保守可能なPythonコードを書くことは不可欠です。常にPEP 8スタイルガイドに従い、意味のある変数名を使用し、関数の包括的なドキュメント文字列を作成してください。",
        "language": "Japanese"
    },
]

# User profile names
USER_NAMES = [
    ("john_dev", "John", "Developer"),
    ("maria_code", "Maria", "Garcia"),
    ("alex_tech", "Alex", "Chen"),
    ("emma_python", "Emma", "Johnson"),
    ("carlos_web", "Carlos", "Rodriguez"),
    ("fatima_code", "Fatima", "Ahmed"),
    ("luca_dev", "Luca", "Rossi"),
    ("yuki_tech", "Yuki", "Tanaka"),
    ("sophia_dev", "Sophia", "Mueller"),
    ("ravi_code", "Ravi", "Patel"),
]

def download_profile_picture(user_id):
    """Download a random avatar from UI Avatars service"""
    try:
        avatar_url = f"https://ui-avatars.com/api/?name=User+{user_id}&size=300&background=random&color=fff"
        response = requests.get(avatar_url, timeout=10)
        if response.status_code == 200:
            return BytesIO(response.content)
    except Exception as e:
        print(f"  ⚠ Failed to download profile picture: {str(e)}")
    return None

def create_default_picture():
    """Create a simple default picture if download fails"""
    try:
        img = Image.new('RGB', (300, 300), color=(73, 109, 137))
        byte_arr = BytesIO()
        img.save(byte_arr, format='JPEG')
        byte_arr.seek(0)
        return byte_arr
    except Exception as e:
        print(f"  ⚠ Failed to create default picture: {str(e)}")
    return None

# Run the script
print("=" * 60)
print("Creating Users and Posts with Profile Pictures")
print("=" * 60)

# Create users
print("\n📝 Creating Users...\n")
users = []
created_user_count = 0

for username, first_name, last_name in USER_NAMES:
    try:
        # Check if user already exists
        if User.objects.filter(username=username).exists():
            user = User.objects.get(username=username)
            print(f"⚠ User '{username}' already exists, skipping creation")
            users.append(user)
            continue
        
        # Create user
        user = User.objects.create_user(
            username=username,
            email=f"{username}@example.com",
            first_name=first_name,
            last_name=last_name,
            password="SecurePassword123!"
        )
        print(f"✓ Created user: {username}")
        users.append(user)
        created_user_count += 1
        
        # Create profile with picture
        print(f"  → Downloading profile picture for {username}...")
        pic_data = download_profile_picture(created_user_count)
        
        if pic_data is None:
            pic_data = create_default_picture()
        
        if pic_data:
            # Create profile
            profile = Profile.objects.create(user=user)
            
            # Save picture
            filename = f"profile_{username}_{uuid.uuid4().hex[:8]}.jpg"
            profile.image.save(filename, pic_data, save=True)
            print(f"  ✓ Profile picture saved")
        else:
            # Create profile with default picture
            profile = Profile.objects.create(user=user)
            print(f"  ⚠ Using default picture")
    
    except Exception as e:
        print(f"✗ Error creating user '{username}': {str(e)}")

# Create posts
print("\n📮 Creating Posts...\n")
post_count = 0

for i, post_data in enumerate(POSTS_DATA):
    try:
        # Randomly select a user
        user = random.choice(users)
        
        # Create post with random timestamp (last 30 days)
        days_ago = random.randint(0, 30)
        hours_ago = random.randint(0, 23)
        minutes_ago = random.randint(0, 59)
        date_posted = timezone.now() - timedelta(
            days=days_ago,
            hours=hours_ago,
            minutes=minutes_ago
        )
        
        post = Post.objects.create(
            title=post_data["title"],
            content=post_data["content"],
            author=user,
            date_posted=date_posted
        )
        
        print(f"✓ Created post: '{post_data['title']}' ({post_data['language']}) by {user.username}")
        post_count += 1
    
    except Exception as e:
        print(f"✗ Error creating post: {str(e)}")

# Summary
print("\n" + "=" * 60)
print("IMPORT SUMMARY")
print("=" * 60)
print(f"✓ Users created: {created_user_count}")
print(f"✓ Posts created: {post_count}")
print(f"Total users in database: {User.objects.count()}")
print(f"Total posts in database: {Post.objects.count()}")
print("=" * 60 + "\n")
