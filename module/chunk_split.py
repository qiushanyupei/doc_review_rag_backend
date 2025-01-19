def chunk_text_by_delimiter(text, delimiter='\n\n', chunk_size=512):
    # 按自定义分隔符分割
    #chunk for chunk in text.split(delimiter) if chunk.strip()
    chunks =  [text]
    # 进一步将每个chunk限制为最大长度
    result = []
    for chunk in chunks:
        # 如果单个chunk长度超过最大限制，按chunk_size拆分
        while len(chunk) > chunk_size:
            result.append(chunk[:chunk_size])
            chunk = chunk[chunk_size:]  # 剩下的部分继续拆分
        if chunk:  # 如果剩余部分不为空
            result.append(chunk)

    return result

