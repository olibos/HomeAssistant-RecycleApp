"""RecycleApp Constants."""

from base64 import b64encode
from typing import Final

DOMAIN: Final = "recycle_app"

COLLECTION_TYPES: Final = {
    # Biodegradable waste
    "5d610b86162c063cc0400108": '<svg xmlns="http://www.w3.org/2000/svg" width="128" height="128" style="shape-rendering:geometricPrecision;text-rendering:geometricPrecision;image-rendering:optimizeQuality;fill-rule:evenodd;clip-rule:evenodd;background:##COLOR##"><path style="opacity:.83" fill="#fefffe" d="M51.5-.5h24c27.667 7 45 24.333 52 52v24c-7 27.667-24.333 45-52 52h-24c-27.667-7-45-24.333-52-52v-24c7-27.667 24.333-45 52-52Zm-17 45c5.084.555 10.084-.279 15-2.5a161.05 161.05 0 0 0 15-8c1.939-.908 2.939-2.408 3-4.5a305.123 305.123 0 0 0-19 5c5.267-3.644 10.6-7.31 16-11l-1.5-1c-1.8.82-3.634 1.486-5.5 2 1.237-2.745 3.07-5.078 5.5-7 .688-.832.521-1.498-.5-2a198.236 198.236 0 0 0-18.5 14c-.667-.667-.667-1.333 0-2 4.24-3.197 6.906-7.197 8-12-.718.95-1.55 1.117-2.5.5 1.211-.893 1.211-1.726 0-2.5-2.049 1.382-3.715 3.048-5 5a4.932 4.932 0 0 0-.5-3l-4 4a101.344 101.344 0 0 1-14 19c-1.726-1.076-3.56-1.243-5.5-.5a34.692 34.692 0 0 0-7.5 6.5 266.691 266.691 0 0 0-10 24C2.25 35.255 17.75 13.755 49.5 4c29.16-5.068 51.66 4.765 67.5 29.5 13.241 28.726 8.741 54.226-13.5 76.5-9.687 7.427-20.52 12.261-32.5 14.5-7.525-5.648-9.859-12.981-7-22a80.005 80.005 0 0 0 14-16 107.303 107.303 0 0 1 9-4c.635-2.135.301-4.135-1-6a57.203 57.203 0 0 0-9.5-8.5 124.641 124.641 0 0 0-16 2.5 83.387 83.387 0 0 0 0-25c-1.788-.285-3.455.048-5 1 2.903 7.54 3.403 15.207 1.5 23-8.297-9.911-17.297-10.578-27-2-.952 3.615.381 5.948 4 7A66.18 66.18 0 0 1 44.5 91c-4.653 4.44-6.153 9.94-4.5 16.5-2.464 3.298-5.63 5.632-9.5 7-11.204-7.25-19.204-17.083-24-29.5A358.694 358.694 0 0 1 16 69.5c2.559-3.031 5.726-5.198 9.5-6.5a20.644 20.644 0 0 0 5-7c3.975.025 5.975-1.975 6-6a36.899 36.899 0 0 1-2-5.5Zm56 1a2.428 2.428 0 0 1 2 .5c-.752.67-1.086 1.504-1 2.5-.904-.709-1.237-1.709-1-3Zm3 7a54.998 54.998 0 0 0 6 10.5c-.638 1.707-.638 3.54 0 5.5-2.295-3.686-4.128-7.687-5.5-12a9.468 9.468 0 0 0-2.5-1.5c1.256-.417 1.923-1.25 2-2.5Zm-61 17c2.963-2.978 6.63-4.645 11-5l18 9 12-3c4.667 2.667 8.333 6.333 11 11-14.774 1.539-28.44-1.628-41-9.5a156.253 156.253 0 0 0-11-2.5Zm67-1c1.424 2.014 2.09 4.348 2 7-.558-2.093-1.89-3.593-4-4.5 1.256-.417 1.923-1.25 2-2.5Z"/><path style="opacity:.878" fill="#fefffe" d="M74.5 14.5c2.49-.202 4.823.298 7 1.5 4.032 5.556 9.032 7.223 15 5 3.03 3.988 4.864 8.488 5.5 13.5 2.369.227 4.869.393 7.5.5 2.696 7.049 2.363 14.049-1 21 2.817 3.32 3.651 7.153 2.5 11.5a82.697 82.697 0 0 1-6.5 16.5c1.022 6.21.522 12.377-1.5 18.5-1.049 1.607-2.549 2.273-4.5 2a147.234 147.234 0 0 0 4-18.5A254.554 254.554 0 0 1 82 68.5a10.414 10.414 0 0 1-1.5-5 55.59 55.59 0 0 1 1.5-6c-5-3.667-9.333-8-13-13-.667-1.667-.667-3.333 0-5a31.857 31.857 0 0 0 4.5-5c-1.792-5.546-2.292-11.212-1.5-17 .698-1.19 1.531-2.19 2.5-3Zm16 31a2.428 2.428 0 0 1 2 .5c-.752.67-1.086 1.504-1 2.5-.904-.709-1.237-1.709-1-3Zm3 7a54.998 54.998 0 0 0 6 10.5c-.638 1.707-.638 3.54 0 5.5-2.295-3.686-4.128-7.687-5.5-12a9.468 9.468 0 0 0-2.5-1.5c1.256-.417 1.923-1.25 2-2.5Zm6 16c1.424 2.014 2.09 4.348 2 7-.558-2.093-1.89-3.593-4-4.5 1.256-.417 1.923-1.25 2-2.5Z"/></svg>',
    # Green waste
    "5d610b86162c063cc0400107": '<svg xmlns="http://www.w3.org/2000/svg" width="128" height="128" style="background:##COLOR##;shape-rendering:geometricPrecision;text-rendering:geometricPrecision;image-rendering:optimizeQuality;fill-rule:evenodd;clip-rule:evenodd"><path fill="#fefffe" d="M51.5-.5h24c27.667 7 45 24.333 52 52v24c-7.03 27.697-24.364 45.03-52 52h-24c-27.667-7-45-24.333-52-52v-24c7.027-27.693 24.36-45.027 52-52Zm6 2c40.817.819 63.484 21.485 68 62-4.486 40.655-27.153 61.155-68 61.5a61.714 61.714 0 0 1-19-5 29378.764 29378.764 0 0 1 34-16c6.1-4.708 8.434-10.874 7-18.5 18.571-2.613 22.238-11.113 11-25.5a25.556 25.556 0 0 1 5.5-6.5c3.461-4.272 3.795-8.606 1-13a55.305 55.305 0 0 1-8-6l-3-15c-4.219-6.242-8.885-6.575-14-1A252.355 252.355 0 0 1 63.5 31C51.745 34.422 45.579 42.256 45 54.5a77.708 77.708 0 0 0 0 13c-5.308 3.617-8.308 8.617-9 15a132.518 132.518 0 0 0 1.5 24.5 30.68 30.68 0 0 1-2 11.5C5.484 100.3-4.35 74.3 6 40.5c10.169-22.346 27.336-35.346 51.5-39Zm16 58a807.966 807.966 0 0 0-4 5 20.088 20.088 0 0 1 1.5-6c.67.752 1.504 1.086 2.5 1Zm-7 12c-.493 2.319-1.493 4.319-3 6-.163-2.357.003-4.69.5-7 .342 2.12 1.175 2.453 2.5 1Zm-6 20c-.762 1.762-2.096 2.762-4 3 .762-1.762 2.096-2.762 4-3Zm-5 1c-.172.992.162 1.658 1 2a16.627 16.627 0 0 1-5 6c.965-2.993 2.298-5.66 4-8Z" style="opacity:.868"/></svg>',
    # PMD
    "5d610b86162c063cc0400125": '<svg xmlns="http://www.w3.org/2000/svg" width="132" height="128" style="shape-rendering:geometricPrecision;text-rendering:geometricPrecision;image-rendering:optimizeQuality;fill-rule:evenodd;clip-rule:evenodd;background:##COLOR##"><path style="opacity:.857" fill="#fefffe" d="M55.5-.5h24c27.64 6.973 44.973 24.307 52 52v24c-7.027 27.693-24.36 45.027-52 52h-24C18.962 116.442 1.795 91.775 4 53.5c6.466-28.298 23.633-46.298 51.5-54Zm62 51a328.89 328.89 0 0 1-17-.5c-1.708-1.062-2.374-2.229-2-3.5a59.29 59.29 0 0 0-10 3.5c-.597 1.889-.93 3.722-1 5.5a222.833 222.833 0 0 1-11 4.5 30.139 30.139 0 0 0-3 3.5 1280.974 1280.974 0 0 0 22 54.5c-11.653 5.996-23.986 7.996-37 6L70 108.5c2.656-4.067 4.156-8.233 4.5-12.5-1.23-5.792-4.23-10.459-9-14 2.765-2.966 2.432-5.633-1-8-3.304-1.042-5.47.125-6.5 3.5-7.769-6.522-15.435-6.522-23 0a414.343 414.343 0 0 0-16 23c-5.448-7.564-9.281-15.898-11.5-25a878.836 878.836 0 0 1 31-13c1.299-.59 2.132-1.59 2.5-3 1.507 1.035 3.007.868 4.5-.5a148.523 148.523 0 0 0 15-20.5c.722.417 1.222 1.084 1.5 2 3.342-.587 6.176-2.087 8.5-4.5a78.42 78.42 0 0 1-4-11.5 25.936 25.936 0 0 0-9 3.5c-.43.92-.764 1.753-1 2.5a95.452 95.452 0 0 0-26-3.5L28 29.5c-1.011-.837-2.178-1.17-3.5-1 .171 3.297-.495 3.63-2 1a32.145 32.145 0 0 1-7 3C24.678 16.056 38.678 6.223 57.5 3 90.726-.143 113.56 13.69 126 44.5a65.243 65.243 0 0 1 2 25 597.7 597.7 0 0 0-7.5-18c-.825-.886-1.825-1.219-3-1Zm-63 32c.531 2.124 1.864 3.624 4 4.5 1.077.47 2.077.303 3-.5-1.993 5.104-4.826 5.77-8.5 2-.739-2.38-.239-4.38 1.5-6Z"/></svg>',
    # Paper
    "5d610b86162c063cc0400123": '<svg xmlns="http://www.w3.org/2000/svg" width="128" height="128" style="shape-rendering:geometricPrecision;text-rendering:geometricPrecision;image-rendering:optimizeQuality;fill-rule:evenodd;clip-rule:evenodd;background:##COLOR##"><path style="opacity:.866" fill="#fefffe" d="M51.5-.5h24c27.667 7 45 24.333 52 52v24c-7 27.667-24.333 45-52 52h-24c-27.667-7-45-24.333-52-52v-24c7.004-27.67 24.337-45.004 52-52Zm-34 82h-3c-1.274 3.881-3.107 7.548-5.5 11-11.542-24.414-9.208-47.414 7-69C41.133-1.271 68.966-4.771 99.5 13c21.945 17.498 29.778 39.998 23.5 67.5-11.702 32.037-34.536 46.537-68.5 43.5a157.334 157.334 0 0 0 9-18.5 1199.835 1199.835 0 0 1-33-8.5c-1.122-3.409-1.289-6.909-.5-10.5a168.19 168.19 0 0 1 1.5 8 598.325 598.325 0 0 1 41.5 13c-.55-4.605-1.05-9.271-1.5-14a76.94 76.94 0 0 0 10-1 48.86 48.86 0 0 0-6-13.5 79.915 79.915 0 0 0-11 1 35.266 35.266 0 0 0 3-10.5 54709.7 54709.7 0 0 1-42-13 49.285 49.285 0 0 1-2 11l-10 1a102.343 102.343 0 0 0 4 13Zm56-53c-3.527 1.352-6.693 3.352-9.5 6-.684-1.284-.517-2.45.5-3.5a45.785 45.785 0 0 1 9-2.5Zm-56 53c2.217.869 4.55 1.202 7 1-2.1 1.112-4.433 1.778-7 2v-3Zm7 1c1.535-1.288 3.201-1.288 5 0-.124.607-.457.94-1 1-1.068-.934-2.401-1.268-4-1Z"/><path style="opacity:.934" fill="#fefffe" d="M68.5 20.5a3321.78 3321.78 0 0 0 11-8l8.5 11a241.123 241.123 0 0 1 11.5-5 1371.189 1371.189 0 0 1 19 47.5c-.944 1.477-2.277 2.477-4 3a1762.807 1762.807 0 0 0-31 12.5 958.118 958.118 0 0 1-14-32 78.853 78.853 0 0 0 6 19l-1 1a696.41 696.41 0 0 1-37-25 820.72 820.72 0 0 1 21.5-32c3.587 2.347 6.754 5.013 9.5 8Zm5 8a45.785 45.785 0 0 0-9 2.5c-1.017 1.05-1.184 2.216-.5 3.5 2.807-2.648 5.973-4.648 9.5-6Z"/></svg>',
    # Non-recyclable waste bag
    "5d610b86162c063cc0400112": '<svg xmlns="http://www.w3.org/2000/svg" width="128" height="128" style="shape-rendering:geometricPrecision;text-rendering:geometricPrecision;image-rendering:optimizeQuality;fill-rule:evenodd;clip-rule:evenodd"><path style="opacity:1" fill="##COLOR##" d="M-.5-.5h53c-27.97 7.303-45.636 24.97-53 53v-53ZM73.5-.5h54v53c-7.439-28.439-25.439-46.106-54-53Z"/><path style="opacity:1" fill="#fbfbfb" d="M52.5-.5h21c28.561 6.894 46.561 24.561 54 53v21c-7.352 30.354-26.352 48.354-57 54h-18c-28.404-7.405-46.07-25.405-53-54v-21c7.364-28.03 25.03-45.697 53-53Z"/><path style="opacity:1" fill="##COLOR##" d="M54.5 1.5c37.754-1.058 61.254 16.609 70.5 53 1.732 19.429-3.768 36.429-16.5 51l-1-4.5a50.884 50.884 0 0 0 1.5-16.5C104.504 73.013 98.004 62.847 89.5 54l-18-4.5v-6c7.495.464 13.495-2.203 18-8a43.079 43.079 0 0 0-1.5-5A119.948 119.948 0 0 1 75.5 17c-6.317-.54-12.484-1.04-18.5-1.5a40.778 40.778 0 0 0-5.5 2.5c3.712 5.258 5.88 11.092 6.5 17.5 10.164 10.83 7.664 15.33-7.5 13.5-9.594 1.8-17.927 5.966-25 12.5a146.609 146.609 0 0 0-12 38C-5.99 67.31-1.656 38.81 26.5 14c8.561-6.118 17.895-10.285 28-12.5Z"/><path style="opacity:1" fill="#7e7e7e" d="M57.5 52.5c4.335.417 8.668.917 13 1.5a246.85 246.85 0 0 0 19 9c9.85 11.99 9.182 12.99-2 3a140.522 140.522 0 0 1-14-7.5l-1 1a41.1 41.1 0 0 1 1.5 17 101.183 101.183 0 0 0-8.5-17 14.974 14.974 0 0 0-3.5 3 121.436 121.436 0 0 1-7 13c-.48-4.105.02-8.105 1.5-12a4.452 4.452 0 0 0-2-1.5l5-5a135.949 135.949 0 0 0-15 6 252.218 252.218 0 0 0-11 15.5c1.005-5.814 3.172-11.481 6.5-17a436.678 436.678 0 0 1 17.5-9Z"/><path style="opacity:1" fill="##COLOR##" d="M-.5 73.5c6.93 28.595 24.596 46.595 53 54h-53v-54ZM127.5 73.5v54h-57c30.648-5.646 49.648-23.646 57-54Z"/></svg>',
    # Pruning waste
    "5d610b86162c063cc0400127": '<svg xmlns="http://www.w3.org/2000/svg" width="128" height="128" style="background:##COLOR##;shape-rendering:geometricPrecision;text-rendering:geometricPrecision;image-rendering:optimizeQuality;fill-rule:evenodd;clip-rule:evenodd"><path style="opacity:.847" fill="#fefffe" d="M51.5-.5h24c27.667 7 45 24.333 52 52v24c-7.004 27.671-24.337 45.004-52 52h-24c-27.667-7-45-24.333-52-52v-24c7-27.667 24.333-45 52-52Zm23 72a147.919 147.919 0 0 1 6.5-31 16.25 16.25 0 0 0 0-8 356.872 356.872 0 0 0-5.5-14c-3.946-.684-7.946-.684-12 0a25.936 25.936 0 0 0 3.5 9 36.54 36.54 0 0 1 1.5 9.5 404.565 404.565 0 0 1-9 44.5c-1.15 1.231-2.317 1.231-3.5 0l-5-14a38.9 38.9 0 0 0-5.5-5c6.612-6.71 8.779-14.71 6.5-24a44.757 44.757 0 0 0-6.5-14c-10.719 10.109-12.719 21.775-6 35l-1.5 1A37.155 37.155 0 0 0 25.5 59c-1.536 1.6-2.036 3.433-1.5 5.5 7.083-.58 13.917.92 20.5 4.5 8.215 9.349 6.549 11.849-5 7.5-10.47 2.163-18.804 7.496-25 16a4.938 4.938 0 0 0 1 2.5c11.32 3.716 21.986 2.383 32-4a35.94 35.94 0 0 0 3.5-4.5l3 3a161.36 161.36 0 0 1-1.5 35C13.242 113.002-2.925 87.002 4 46.5c9.946-28.266 29.946-43.266 60-45 40.39 4.721 60.723 27.388 61 68-4.494 29.66-21.327 47.994-50.5 55a338.065 338.065 0 0 1-.5-45L87.5 68c16.242-3.738 24.576-13.904 25-30.5-16.126 1.293-25.293 9.96-27.5 26a114.159 114.159 0 0 1-10.5 8Z"/></svg>',
    # Non-recyclable waste
    "5d610b86162c063cc0400133": '<svg xmlns="http://www.w3.org/2000/svg" width="128" height="128" style="shape-rendering:geometricPrecision;text-rendering:geometricPrecision;image-rendering:optimizeQuality;fill-rule:evenodd;clip-rule:evenodd;background:##COLOR##"><path style="opacity:.843" fill="#fefffe" d="M51.5-.5h24c27.667 7 45 24.333 52 52v24c-7 27.667-24.333 45-52 52h-24c-27.667-7-45-24.333-52-52v-24c7-27.667 24.333-45 52-52Zm7 82c1.333-.333 1.333-.667 0-1a741.833 741.833 0 0 0 7-20.5c9.66-.5 19.328-.666 29-.5.213-1.644-.12-3.144-1-4.5A519.167 519.167 0 0 0 48 38.5c-5 .328-8.667 2.662-11 7a699.562 699.562 0 0 1-7.5 25 630.581 630.581 0 0 0 26 10 961.686 961.686 0 0 1-27-5 1054.273 1054.273 0 0 1 2.5 40C5.56 97.183-2.773 72.85 6 42.5c10.768-25.308 29.935-38.642 57.5-40 33.713 2.214 53.88 19.88 60.5 53 2.269 22.885-5.398 41.551-23 56 .829-7.634 1.996-15.3 3.5-23a4.932 4.932 0 0 0-1-2.5 289.236 289.236 0 0 0-34 0 4.938 4.938 0 0 0-1 2.5 534.523 534.523 0 0 0 7 34.5 28.04 28.04 0 0 0-5 1.5 785.926 785.926 0 0 1-12-43Zm-13 14a412.493 412.493 0 0 1 18 28c-8.5 1.194-16.5-.306-24-4.5a134.998 134.998 0 0 0 6-23.5Z"/><path style="opacity:.897" fill="#fefffe" d="M62.5 16.5c9.78.958 13.614 6.291 11.5 16-5.372 6.945-11.372 7.612-18 2-4.277-8.43-2.11-14.43 6.5-18Z"/><path style="opacity:.927" fill="#fefffe" d="M58.5 80.5h-3a630.581 630.581 0 0 1-26-10 699.562 699.562 0 0 0 7.5-25c2.333-4.338 6-6.672 11-7A519.167 519.167 0 0 1 93.5 55c.88 1.356 1.213 2.856 1 4.5-9.672-.166-19.34 0-29 .5a741.833 741.833 0 0 1-7 20.5Z"/><path style="opacity:.832" fill="#fefffe" d="M85.5 66.5c3.585-.231 6.752.769 9.5 3 1.079 3.805.412 7.138-2 10a18.088 18.088 0 0 0-3.5-2c-3.627 1.575-6.793.908-9.5-2-.699-2.822.468-4.488 3.5-5 .862-1.266 1.53-2.6 2-4Z"/></svg>',
    # Glass
    "5d610b86162c063cc0400110": '<svg xmlns="http://www.w3.org/2000/svg" width="128" height="128" style="background:##COLOR##;shape-rendering:geometricPrecision;text-rendering:geometricPrecision;image-rendering:optimizeQuality;fill-rule:evenodd;clip-rule:evenodd"><path fill="#fefffe" d="M51.5-.5h24c27.667 7 45 24.333 52 52v24c-7 27.667-24.333 45-52 52h-24c-27.658-6.991-44.991-24.325-52-52v-24c7-27.667 24.333-45 52-52Zm71 57a58.703 58.703 0 0 0-19.5-5c-3.168.043-6.168.71-9 2A509.893 509.893 0 0 1 67.5 26c-7.726-.21-13.226 3.29-16.5 10.5-2.108 5.802.058 9.468 6.5 11 4.678-1.67 8.678-4.337 12-8-1.808 4.603-4.808 8.27-9 11a607.912 607.912 0 0 1 21 20.5c10.57.098 15.736-5.069 15.5-15.5 3.965 4.706 3.965 9.706 0 15-5.034 7.462-11.534 9.462-19.5 6-.258 15.329 5.409 28.162 17 38.5-16.286 8.993-33.286 10.66-51 5a237.417 237.417 0 0 1 17-19.5c-11.388-1.141-20.221-6.808-26.5-17a59.29 59.29 0 0 1-3.5-10 15.681 15.681 0 0 1 2-4c2.153 8.018 6.82 14.852 14 20.5 5.105 4.35 10.772 5.35 17 3 6.4-6.545 6.567-13.379.5-20.5-5.04-7.047-11.707-11.714-20-14-4.751.085-7.751 2.418-9 7a3.646 3.646 0 0 0-1.5-1 28.04 28.04 0 0 1-5 1.5 550.72 550.72 0 0 1-20 19.5C-.947 58.992 4.72 36.159 25.5 17c25.339-17.999 50.672-17.999 76 0 12.399 10.299 19.399 23.466 21 39.5Zm-74 6c7.667 3 13 8.333 16 16-.722.418-1.222 1.084-1.5 2-3.21-7.37-8.044-13.37-14.5-18Zm-7 2c1.67.251 3.17.918 4.5 2l1-2c6.461 4.293 11.295 9.96 14.5 17 .774 1.211 1.607 1.211 2.5 0 .797 1.759.63 3.425-.5 5-11.044-3.711-18.378-11.044-22-22Z" style="opacity:.89"/></svg>',
    # Christmas trees
    "5d610b86162c063cc0400102": '<svg xmlns="http://www.w3.org/2000/svg" width="128" height="128" style="background:##COLOR##;shape-rendering:geometricPrecision;text-rendering:geometricPrecision;image-rendering:optimizeQuality;fill-rule:evenodd;clip-rule:evenodd"><path fill="#fefffe" d="M51.5-.5h24c27.667 7 45 24.333 52 52v24c-7 27.667-24.333 45-52 52h-24c-27.658-6.991-44.991-24.325-52-52v-24c7-27.667 24.333-45 52-52Zm7 4c36.277.45 57.777 18.45 64.5 54 1.177 31.49-12.99 52.656-42.5 63.5a30.463 30.463 0 0 1-9 1.5v-16c9.751-.806 18.751-3.806 27-9-8.776-2.443-15.11-7.776-19-16a96.39 96.39 0 0 1 11-2.5c.457-.414.79-.914 1-1.5-8.549-3.715-14.549-9.882-18-18.5a52.204 52.204 0 0 0 10-1.5c-8.915-4.45-15.581-11.117-20-20-4.326 8.993-10.993 15.66-20 20l10 2c-3.674 8.34-9.674 14.34-18 18 3.75 1.941 7.75 3.274 12 4-3.684 8.36-10.017 13.693-19 16 8.249 5.194 17.249 8.194 27 9v16c-32.16-6.499-49.494-26.166-52-59 3.12-34.115 21.454-54.115 55-60Z" style="opacity:.878"/></svg>',
    # Textiles
    "5d610b86162c063cc0400131": '<svg xmlns="http://www.w3.org/2000/svg" width="128" height="128" style="background:##COLOR##;shape-rendering:geometricPrecision;text-rendering:geometricPrecision;image-rendering:optimizeQuality;fill-rule:evenodd;clip-rule:evenodd"><path fill="#fefffe" d="M51.5-.5h24q41.46 10.46 52 52v24q-10.546 41.545-52 52h-24q-41.46-10.46-52-52v-24q10.54-41.54 52-52m6 2q61.226 1.229 68 62-5.497 56.497-62 62-56.503-5.503-62-62 4.497-52.486 56-62" style="opacity:.66"/><path fill="#fefffe" d="M48.5 25.5h8q-3.727 15.02 11 11.5 5.624-4.563 2-10.5 4.419-1.732 9-.5 16.438 8.196 29 21.5a231 231 0 0 0-11 14.5q-5.685-.363-10-4.5a530 530 0 0 0-1 46h-45q1.467-23.01 0-46a48.5 48.5 0 0 0-7 4.5q-1.5 1-3 0a366 366 0 0 0-11-14.5q12.858-13.383 29-22" style="opacity:.962"/></svg>',
    # Waste Container
    "609a4b94e85d9b1e58b530e8": '<svg xmlns="http://www.w3.org/2000/svg" width="128" height="128" style="background:##COLOR##;shape-rendering:geometricPrecision;text-rendering:geometricPrecision;image-rendering:optimizeQuality;fill-rule:evenodd;clip-rule:evenodd"><path fill="#fefffe" d="M52.5-.5h22q43.014 10.013 53 53v22q-10.014 43.014-53 53h-22q-43.013-10.014-53-53v-22q10.013-43.013 53-53m9 4q56.435 4.184 62 60.5-5.953 54.453-60.5 59.5Q8.547 117.547 3.5 63q5.625-52.872 58-59.5m7 95q-.5 1.5-2 2 0-2 2-2m-2 2q-2 5 0 10-.925-.166-1.5-1a16.25 16.25 0 0 1 0-8q.575-.834 1.5-1" style="opacity:.805"/><path fill="#fefffe" d="M47.5 16.5q5.865-.356 11 2.5l27 13q5.8 5.31 0 10.5a1226 1226 0 0 1-42-20.5q1.482-3.25 4-5.5" style="opacity:.89"/><path fill="#fefffe" d="M39.5 43.5h47v9h-47z" style="opacity:.959"/><path fill="#fefffe" d="M70.5 97.5q-1.487-.257-2 1-2 0-2 2-.925.166-1.5 1a16.25 16.25 0 0 0 0 8q.575.834 1.5 1-.128 1.494 1 2.5a64.2 64.2 0 0 1-16 0 6.98 6.98 0 0 1-3.5-2.5Q44.5 82.735 41.5 55a925 925 0 0 1 43-.5 1232 1232 0 0 1-5 44q-4.47-3.009-9-1" style="opacity:.965"/><path fill="#fefffe" d="M70.5 97.5q13.884.305 9 13-6.551 5.982-13 0-2-5 0-10 1.5-.5 2-2 1.487.257 2-1" style="opacity:.88"/></svg>',
}

# Some cities use another icon for the same purpose, to avoid duplication
# I'll just make alias entries

# Wetteren (https://github.com/olibos/HomeAssistant-RecycleApp/issues/4)
COLLECTION_TYPES["5d610b86162c063cc0400111"] = COLLECTION_TYPES[
    "5d610b86162c063cc0400108"
]

DEFAULT_DATE_FORMAT: Final = "%Y-%m-%d"


def get_icon(collection_type_id: str, color: str):
    """Get the specified collection type icon in the specified color."""
    svg = COLLECTION_TYPES.get(collection_type_id)
    if svg is None:
        return None
    return f'data:image/svg+xml;base64,{b64encode(svg.replace("##COLOR##", color).encode()).decode()}'
