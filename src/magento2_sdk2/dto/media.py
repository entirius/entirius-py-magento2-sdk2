# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

from dataclasses import dataclass

from magento2_sdk2.dto import DTO


@dataclass
class VideoContent(DTO):
    media_type: str
    video_provider: str
    video_url: str
    video_title: str | None
    video_description: str | None
    video_metadata: str | None


@dataclass
class ExtensionAttributes:
    video_content: VideoContent | None = None

    @staticmethod
    def factory(data: dict) -> "ExtensionAttributes":
        video_content = data.get("video_content")
        if video_content:
            video_content = VideoContent(**video_content)
        return ExtensionAttributes(video_content=video_content)


@dataclass
class MediaContent(DTO):
    base64_encoded_data: str
    type: str
    name: str


@dataclass
class Media(DTO):
    media_type: str
    file: list[str] | None = None
    types: list[str] | None = None
    label: str | None = None
    position: int = 0
    disabled: bool = False
    content: MediaContent | None = None
    extension_attributes: ExtensionAttributes | None = None

    def is_picture(self) -> bool:
        return self.media_type == "image"

    def is_video(self) -> bool:
        return self.media_type == "external-video"

    @staticmethod
    def factory(data: dict) -> "Media":
        data = data.copy()
        data.pop("id", None)  # Don't need ID
        extension_attributes = data.pop("extension_attributes", None)
        if extension_attributes:
            extension_attributes = ExtensionAttributes.factory(extension_attributes)
        return Media(extension_attributes=extension_attributes, **data)
