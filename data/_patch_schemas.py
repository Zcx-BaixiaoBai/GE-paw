from pathlib import Path
p = Path('src/agentscope_runtime/engine/schemas/agent_schemas.py')
data = p.read_bytes()
# Normalize to LF for matching
data = data.replace(b'\r\n', b'\n')

old1 = b'''class ImageContent(BaseModel):
    """Image content."""

    type: ContentType = Field(default=ContentType.IMAGE)
    image_url: str = Field(default="")
'''
new1 = b'''class ImageContent(BaseModel):
    """Image content."""

    type: ContentType = Field(default=ContentType.IMAGE)
    image_url: Optional[str] = Field(default=None)
    data: Optional[str] = Field(default=None)
'''
print('ImageContent found:', old1 in data)
data = data.replace(old1, new1)

old2 = b'''class AudioContent(BaseModel):
    """Audio content."""

    type: ContentType = Field(default=ContentType.AUDIO)
    audio_url: str = Field(default="")
'''
new2 = b'''class AudioContent(BaseModel):
    """Audio content."""

    type: ContentType = Field(default=ContentType.AUDIO)
    audio_url: Optional[str] = Field(default=None)
    data: Optional[str] = Field(default=None)
'''
print('AudioContent found:', old2 in data)
data = data.replace(old2, new2)

old3 = b'''class VideoContent(BaseModel):
    """Video content."""

    type: ContentType = Field(default=ContentType.VIDEO)
    video_url: str = Field(default="")
'''
new3 = b'''class VideoContent(BaseModel):
    """Video content."""

    type: ContentType = Field(default=ContentType.VIDEO)
    video_url: Optional[str] = Field(default=None)
    data: Optional[str] = Field(default=None)
'''
print('VideoContent found:', old3 in data)
data = data.replace(old3, new3)

old4 = b'''class FileContent(BaseModel):
    """File content."""

    type: ContentType = Field(default=ContentType.FILE)
    file_url: str = Field(default="")
    filename: str = Field(default="")
'''
new4 = b'''class FileContent(BaseModel):
    """File content."""

    type: ContentType = Field(default=ContentType.FILE)
    file_url: Optional[str] = Field(default=None)
    file_id: Optional[str] = Field(default=None)
    data: Optional[str] = Field(default=None)
    filename: str = Field(default="")
'''
print('FileContent found:', old4 in data)
data = data.replace(old4, new4)

p.write_bytes(data)
print('done')
