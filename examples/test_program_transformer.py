import os
import sys
import ast
import astor
from scalpel.rewriter import Rewriter


src1 = '''
def get_vid_from_url(url):
    """Extracts video ID from URL."""
    return match1(url, r'youtu\.be/([^?/]+)') or \
           match1(url, r'youtube\.com/embed/([^/?]+)') or \
           match1(url, r'youtube\.com/v/([^/?]+)') or \
           match1(url, r'youtube\.com/watch/([^/?]+)') or \
           parse_query_param(url, 'v') or \
           parse_query_param(parse_query_param(url, 'u'), 'v')

'''
src2 = '''def sina_xml_to_url_list(xml_data):
    """str->list
    Convert XML to URL List.
    From Biligrab.
    """
    rawurl = []
    dom = parseString(xml_data)
    for node in dom.getElementsByTagName('durl'):
        url = node.getElementsByTagName('url')[0]
        rawurl.append(url.childNodes[0].data)
    return rawurl
'''
src3 = '''
def makeMimi(upid):
    """From http://cdn37.atwikiimg.com/sitescript/pub/dksitescript/FC2.site.js
    Also com.hps.util.fc2.FC2EncrptUtil.makeMimiLocal
    L110"""
    strSeed = "gGddgPfeaf_gzyr"
    prehash = upid + "_" + strSeed
    return md5(prehash.encode('utf-8')).hexdigest()

'''

src4 = '''
def fc2video_download(url, output_dir='.', merge=True, info_only=False, **kwargs):
    """wrapper"""
    # 'http://video.fc2.com/en/content/20151021bTVKnbEw'
    # 'http://xiaojiadianvideo.asia/content/20151021bTVKnbEw'
    # 'http://video.fc2.com/ja/content/20151021bTVKnbEw'
    # 'http://video.fc2.com/tw/content/20151021bTVKnbEw'
    hostname = urlparse(url).hostname
    if not ('fc2.com' in hostname or 'xiaojiadianvideo.asia' in hostname):
        return False
    upid = match1(url, r'.+/content/(\w+)')

    fc2video_download_by_upid(upid, output_dir, merge, info_only)
'''

src5 = '''
def dailymotion_download(url, output_dir='.', merge=True, info_only=False, **kwargs):
    """Downloads Dailymotion videos by URL.
    """

    html = get_content(rebuilt_url(url))
    info = json.loads(match1(html, r'qualities":({.+?}),"'))
    title = match1(html, r'"video_title"\s*:\s*"([^"]+)"') or \
            match1(html, r'"title"\s*:\s*"([^"]+)"')
    title = unicodize(title)

    for quality in ['1080', '720', '480', '380', '240', '144', 'auto']:
        try:
            real_url = info[quality][1]["url"]
            if real_url:
                break
        except KeyError:
            pass

    mime, ext, size = url_info(real_url)

    print_info(site_info, title, mime, size)
    if not info_only:
        download_urls([real_url], title, ext, size, output_dir=output_dir, merge=merge)

'''
src6 = '''
def dictify(r, root=True):
    """http://stackoverflow.com/a/30923963/2946714"""
    if root:
        return {r.tag: dictify(r, False)}
    d = copy(r.attrib)
    if r.text:
        d["_text"] = r.text
    for x in r.findall("./*"):
        if x.tag not in d:
            d[x.tag] = []
        d[x.tag].append(dictify(x, False))
    return d

'''
src7 = '''
def ucas_download_single(url, output_dir='.', merge=False, info_only=False, **kwargs):
    """video page"""
    html = get_content(url)
    # resourceID is UUID
    resourceID = re.findall(r'resourceID":"([0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12})', html)[0]
    assert resourceID != '', 'Cannot find resourceID!'

    title = match1(html, r'<div class="bc-h">(.+)</div>')
    url_lists = _ucas_get_url_lists_by_resourceID(resourceID)
    assert url_lists, 'Cannot find any URL of such class!'

    for k, part in enumerate(url_lists):
        part_title = title + '_' + str(k)
        print_info(site_info, part_title, 'flv', 0)
        if not info_only:
            download_urls(part, part_title, 'flv', total_size=None, output_dir=output_dir, merge=merge)

'''
src7 = '''
def ucas_download_playlist(url, output_dir='.', merge=False, info_only=False, **kwargs):
    """course page"""
    html = get_content(url)

    parts = re.findall(r'(getplaytitle.do\?.+)"', html)
    assert parts, 'No part found!'

    for part_path in parts:
        ucas_download('http://v.ucas.ac.cn/course/' + part_path, output_dir=output_dir, merge=merge,
                      info_only=info_only)

'''
src8 = '''
def sina_download_by_vid(vid, title=None, output_dir='.', merge=True, info_only=False):
    """Downloads a Sina video by its unique vid.
    http://video.sina.com.cn/
    """
    xml = api_req(vid)
    urls, name, size = video_info(xml)
    if urls is None:
        log.wtf(name)
    title = name
    print_info(site_info, title, 'flv', size)
    if not info_only:
        download_urls(urls, title, 'flv', size, output_dir=output_dir, merge=merge)

'''
src9 = '''
def sina_download_by_vkey(vkey, title=None, output_dir='.', merge=True, info_only=False):
    """Downloads a Sina video by its unique vkey. http://video.sina.com/
    """

    url = 'http://video.sina.com/v/flvideo/%s_0.flv' % vkey
    type, ext, size = url_info(url)

    print_info(site_info, title, 'flv', size)
    if not info_only:
        download_urls([url], title, 'flv', size, output_dir=output_dir, merge=merge)


'''

src10 = '''
def sina_download_by_vkey(vkey, title=None, output_dir='.', merge=True, info_only=False):
    if not info_only:
        download_urls([url], title, 'flv', size, output_dir=output_dir, merge=merge)

'''

src11 = """
def func(x,y):
    z = 0.
    for i in range(x+y):
        z+=i
    return z
"""

def main():
    rewriter = Rewriter(src11)
    print(src11)
    rewriter.random_var_renaming(new_name = "_renamed_one")
    rewriter.unused_stmt_insertion()
    rewriter.loop_exchange()
    new_src = rewriter.get_src()
    print(new_src)

if __name__ == '__main__':
    main()

