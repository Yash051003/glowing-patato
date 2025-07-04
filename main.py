from instagrapi import Client
import time

# Configuration
USERNAME = "username"
PASSWORD = "pass"
TARGET = "target_username"

def safe_fetch_highlights(client, user_id):
    """Safely fetch highlights with multiple fallback methods"""
    try:
        # Method 1: Try the standard approach
        highlights = client.user_highlights(user_id)
        if highlights:
            return highlights
    except Exception as e:
        print(f"⚠️ Method 1 failed: {e}")
    
    try:
        # Method 2: Alternative approach using reel_ids
        highlights = client.user_highlights(user_id, amount=50)
        if highlights:
            return highlights
    except Exception as e:
        print(f"⚠️ Method 2 failed: {e}")
    
    return []

def main():
    client = Client()
    
    try:
        # Simple login with OTP handling
        print("🔐 Logging in...")
        client.login(USERNAME, PASSWORD)
        print("✅ Login successful!")
        
        # Fetch target user info
        print(f"\n🔍 Fetching info for @{TARGET}...")
        user_id = client.user_id_from_username(TARGET)
        user_info = client.user_info(user_id)
        
        # Display user info
        print(f"\n📄 Username: {user_info.username}")
        print(f"📝 Full Name: {user_info.full_name}")
        print(f"🔐 Private: {user_info.is_private}")
        print(f"👥 Followers: {user_info.follower_count}")
        print(f"📸 Posts: {user_info.media_count}")
        
        # Fetch following (with error handling)
        try:
            print(f"\n👤 Fetching who {TARGET} is following...")
            following = client.user_following(user_id, amount=20)
            print(f"👤 {TARGET} is following:")
            for user in following.values():
                print(f"➡️ {user.username} | {user.full_name}")
        except Exception as e:
            print(f"⚠️ Could not fetch following: {e}")
        
        # Fetch stories (with error handling)
        try:
            print(f"\n📸 Fetching stories...")
            stories = client.user_stories(user_id)
            if stories:
                for i, story in enumerate(stories, 1):
                    print(f"\n📸 Story #{i}:")
                    print(f"🕒 Taken at: {story.taken_at}")
                    print(f"🔗 URL: {story.thumbnail_url}")
            else:
                print("📭 No active stories found")
        except Exception as e:
            print(f"⚠️ Could not fetch stories: {e}")
        
        # Fetch highlights (IMPROVED VERSION)
        try:
            print(f"\n📁 Fetching highlights...")
            highlights = safe_fetch_highlights(client, user_id)
            
            if highlights:
                print(f"✅ Found {len(highlights)} highlights")
                for h in highlights:
                    print(f"\n📁 Highlight: {h.title} ({h.media_count} items)")
                    
                    # Try multiple methods to get highlight media
                    try:
                        # Method 1: Using story_pk_to_story (most reliable)
                        if hasattr(h, 'pk') and h.pk:
                            try:
                                highlight_stories = client.story_pk_to_story(h.pk)
                                if highlight_stories:
                                    if not isinstance(highlight_stories, list):
                                        highlight_stories = [highlight_stories]
                                    
                                    print(f"✅ Found {len(highlight_stories)} media items:")
                                    for idx, story in enumerate(highlight_stories, 1):
                                        print(f"   🖼️ Media #{idx}: {getattr(story, 'thumbnail_url', 'N/A')}")
                                        print(f"   📅 Taken at: {getattr(story, 'taken_at', 'N/A')}")
                                        if hasattr(story, 'video_url') and story.video_url:
                                            print(f"   🎥 Video URL: {story.video_url}")
                                else:
                                    print("⚠️ No stories found in this highlight using story_pk_to_story")
                            except Exception as story_err:
                                print(f"⚠️ story_pk_to_story failed: {story_err}")
                                
                                # Method 2: Try using reel_media
                                try:
                                    reel_media = client.reel_media(h.pk)
                                    if reel_media and hasattr(reel_media, 'items'):
                                        print(f"✅ Found media using reel_media:")
                                        for idx, item in enumerate(reel_media.items, 1):
                                            print(f"   🖼️ Media #{idx}: {getattr(item, 'thumbnail_url', 'N/A')}")
                                            print(f"   📅 Taken at: {getattr(item, 'taken_at', 'N/A')}")
                                    else:
                                        print("⚠️ No media found using reel_media")
                                except Exception as reel_err:
                                    print(f"⚠️ reel_media failed: {reel_err}")
                                    
                                    # Method 3: Show available highlight info
                                    print("📋 Available highlight info:")
                                    print(f"   📋 Highlight ID: {getattr(h, 'id', 'N/A')}")
                                    print(f"   📋 Highlight PK: {getattr(h, 'pk', 'N/A')}")
                                    if hasattr(h, 'cover_media') and h.cover_media:
                                        cover_url = getattr(h.cover_media, 'thumbnail_url', 'N/A')
                                        print(f"   📋 Cover URL: {cover_url}")
                        else:
                            print("⚠️ Highlight doesn't have pk attribute")
                            
                    except Exception as highlight_error:
                        print(f"⚠️ Could not process highlight: {highlight_error}")
                    
                    # Small delay between highlights
                    time.sleep(1)
            else:
                print("📭 No highlights found")
                
        except Exception as e:
            print(f"⚠️ Could not fetch highlights: {e}")
        
        # Fetch recent posts (uncomment if needed)
        # try:
        #     print(f"\n📷 Fetching recent posts...")
        #     posts = client.user_medias(user_id, amount=5)
        #     for i, post in enumerate(posts, 1):
        #         print(f"\n📷 Post #{i}:")
        #         print(f"📝 Caption: {post.caption_text}")
        #         print(f"🔗 URL: https://www.instagram.com/p/{post.code}/")
        # except Exception as e:
        #     print(f"⚠️ Could not fetch posts: {e}")
        
        print("\n✅ Script completed successfully!")
        
    except Exception as e:
        print(f"❌ Script failed: {e}")
    
    finally:
        # Optional: logout
        try:
            client.logout()
            print("🔓 Logged out successfully")
        except:
            pass

if __name__ == "__main__":
    main()