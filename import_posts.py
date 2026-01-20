import json
from django.conf import settings
import django
import os

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project_one.settings')
django.setup()

from blog.models import Post
from django.contrib.auth.models import User

# Load the JSON data
with open('posts.json', 'r') as f:
    posts_data = json.load(f)

# Map old user IDs to new ones (or use the first available users)
existing_users = list(User.objects.all())
user_mapping = {}

# Get the first and second user (if they exist)
for old_id in [1, 2]:
    if len(existing_users) > 0:
        # Use round-robin to distribute posts
        if old_id == 1 and len(existing_users) > 0:
            user_mapping[1] = existing_users[0]
        elif old_id == 2 and len(existing_users) > 1:
            user_mapping[2] = existing_users[1]
        elif old_id == 2 and len(existing_users) == 1:
            user_mapping[2] = existing_users[0]

print(f"Found {len(existing_users)} existing users")
print(f"User mapping: {[(k, v.username) for k, v in user_mapping.items()]}\n")

# Import posts
imported_count = 0
skipped_count = 0

for post_data in posts_data:
    try:
        user_id = post_data['user_id']
        
        # Get the user from mapping
        if user_id in user_mapping:
            user = user_mapping[user_id]
        else:
            # Try to use the first existing user
            if existing_users:
                user = existing_users[0]
            else:
                print(f"✗ No users available - skipping post: {post_data['title']}")
                skipped_count += 1
                continue
        
        # Create and save the Post
        post = Post(
            title=post_data['title'],
            content=post_data['content'],
            author=user
        )
        post.save()
        print(f"✓ Created post: {post.title} (author: {user.username})")
        imported_count += 1
    except Exception as e:
        print(f"✗ Error creating post '{post_data['title']}': {str(e)}")
        skipped_count += 1

print(f"\n✓ Import complete!")
print(f"  Imported: {imported_count}")
print(f"  Skipped: {skipped_count}")
print(f"  Total posts in database: {Post.objects.count()}")
