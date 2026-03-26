import json
import urllib.request
import urllib.parse

searches = {
    'Coffee Leaf Rust': 'Hemileia vastatrix',
    'Coffee Black Rot': 'Koleroga noxia',
    'Coffee Fusarium Root Rot': 'Fusarium oxysporum',
    'Coffee Berry Disease': 'Colletotrichum kahawae',
    'Xylotrechus quadripes': 'Xylotrechus quadripes',
    'Hypothenemus hampei': 'Hypothenemus hampei',
    'Colletotrichum capsici': 'Colletotrichum capsici',
    'Magnaporthe oryzae': 'Magnaporthe oryzae',
}

results = {}

for name, search_term in searches.items():
    print(f"\n{name}: ", end='', flush=True)
    try:
        url = f"https://en.wikipedia.org/api/rest_v1/page/summary/{urllib.parse.quote(search_term)}"
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 (compatible; CropAdvisoryBot/1.0)'})
        with urllib.request.urlopen(req, timeout=5) as response:
            data = json.loads(response.read())
            if data.get('thumbnail') and data['thumbnail'].get('source'):
                img_url = data['thumbnail']['source']
                # Upgrade to larger size
                img_url = img_url.replace('220px', '400px').replace('320px', '400px').replace('330px', '400px')
                results[name] = img_url
                print(f"✓ Found")
            else:
                print(f"No image in summary")
    except Exception as e:
        print(f"Error: {str(e)[:40]}")

print("\n" + "="*70)
print("NEW IMAGE URLS:")
for name, url in results.items():
    print(f"\n{name}:")
    print(f"  {url}")
