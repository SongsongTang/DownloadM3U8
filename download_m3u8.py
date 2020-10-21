import requests

def get_response(url):
    headers = {
                "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.111 Safari/537.36",
            }
    session = requests.Session()
    try:
        response = session.get(url, headers=headers, timeout=30)
        response.raise_for_status()
        return response
    except:
        print("request failed!")
        return None

def get_url(url, response):
    useless_url = url.split("/")[-1]
    front_url = url.replace(useless_url, "")
    url_text = response.text
    url_seg_1 = url_text.split(",\n")[1:]
    url_seg_2 = [us1.split("\n#EXT")[0] for us1 in url_seg_1]
    seg_url = [front_url+us for us in url_seg_2]
    return seg_url

def write_files(seg_response):
    response_content = seg_response.content
    with open("video.mp4", 'ab') as f:
        f.write(response_content)

def main():
    m3u8_url = input("Please input m3u8_url: ")
    m3u8_response = get_response(m3u8_url)
    if m3u8_response:
        seg_url = get_url(m3u8_url, m3u8_response)
    else:
        print("m3u8 request failed")
    i = 0
    while True:
        try:
            seg_response = get_response(seg_url[i])
        except:
            print("Download complete!")
            break
        if seg_response:
            write_files(seg_response)
            print(str(i) + "/" + str(len(seg_url)), end="\r")
            i += 1
        else:
            continue

if __name__ == "__main__":
    main()

