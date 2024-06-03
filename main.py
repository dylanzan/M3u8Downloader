import requests
import os
import aiohttp
import asyncio


def parse_m3u8_url(url: str):
    r = requests.get(url)
    if r.status_code != 200:
        print('m3u8视频下载链接无效')
        return False

    m3u8_list = r.text.split('\n')
    m3u8_list = [i for i in m3u8_list if i and i[0] != '#']

    print("m3u8's list: ", m3u8_list)

    ts_list = []
    for ts_url in m3u8_list:
        ts_url = url.rsplit('/', 1)[0] + '/' + ts_url
        ts_list.append(ts_url)

    print("ts's list: ", ts_list)
    return ts_list


def convert_ts_to_mp4(ts_file_path, mp4_file_path):
    os.system(f'ffmpeg -f concat -safe 0 -i  {ts_file_path} -c copy {mp4_file_path}')


async def download_job(file_path, session, url):
    name = url.split('/')[-1]
    async with session.get(url) as response:
        with open(file_path + "/" + name, 'wb') as f:
            while True:
                chunk = await response.content.read(1024)
                if not chunk:
                    break
                f.write(chunk)


async def download_m3u8_video_async(loop, url, file_path):
    async with aiohttp.ClientSession() as session:
        tasks = [loop.create_task(download_job(file_path, session, url)) for url in url]
        finshed, unfinished = await asyncio.wait(tasks)

        all_results = [r.result() for r in finshed]
        print('所有任务完成:', str(all_results))


if __name__ == '__main__':
    url = 'https://domain.com/mixed.m3u8'
    ts_file_path = 'ts_files/1.txt'
    mp4_file_path = 'mp4_files/1.mp4'

    # ts_url_files=parse_m3u8_url(url)
    # loop=asyncio.get_event_loop()
    # loop.run_until_complete(download_m3u8_video_async(loop,ts_url_files,ts_file_path))
    convert_ts_to_mp4(ts_file_path,mp4_file_path)