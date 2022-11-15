from typing import final


DOMAIN: final = "recycle_app"

COLLECTION_TYPES = {
    "5d610b86162c063cc0400108": {
        "nl": "Groente-, fruit-, tuinafval",
        "fr": "Déchets biodégradables",
        "de": "Bioabfall",
        "en": "Biodegradable waste",
        "image": "data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHdpZHRoPSIxMjgiIGhlaWdodD0iMTI4IiBzdHlsZT0ic2hhcGUtcmVuZGVyaW5nOmdlb21ldHJpY1ByZWNpc2lvbjt0ZXh0LXJlbmRlcmluZzpnZW9tZXRyaWNQcmVjaXNpb247aW1hZ2UtcmVuZGVyaW5nOm9wdGltaXplUXVhbGl0eTtmaWxsLXJ1bGU6ZXZlbm9kZDtjbGlwLXJ1bGU6ZXZlbm9kZDtiYWNrZ3JvdW5kOiM2Mzg5MTkiPjxwYXRoIHN0eWxlPSJvcGFjaXR5Oi44MyIgZmlsbD0iI2ZlZmZmZSIgZD0iTTUxLjUtLjVoMjRjMjcuNjY3IDcgNDUgMjQuMzMzIDUyIDUydjI0Yy03IDI3LjY2Ny0yNC4zMzMgNDUtNTIgNTJoLTI0Yy0yNy42NjctNy00NS0yNC4zMzMtNTItNTJ2LTI0YzctMjcuNjY3IDI0LjMzMy00NSA1Mi01MlptLTE3IDQ1YzUuMDg0LjU1NSAxMC4wODQtLjI3OSAxNS0yLjVhMTYxLjA1IDE2MS4wNSAwIDAgMCAxNS04YzEuOTM5LS45MDggMi45MzktMi40MDggMy00LjVhMzA1LjEyMyAzMDUuMTIzIDAgMCAwLTE5IDVjNS4yNjctMy42NDQgMTAuNi03LjMxIDE2LTExbC0xLjUtMWMtMS44LjgyLTMuNjM0IDEuNDg2LTUuNSAyIDEuMjM3LTIuNzQ1IDMuMDctNS4wNzggNS41LTcgLjY4OC0uODMyLjUyMS0xLjQ5OC0uNS0yYTE5OC4yMzYgMTk4LjIzNiAwIDAgMC0xOC41IDE0Yy0uNjY3LS42NjctLjY2Ny0xLjMzMyAwLTIgNC4yNC0zLjE5NyA2LjkwNi03LjE5NyA4LTEyLS43MTguOTUtMS41NSAxLjExNy0yLjUuNSAxLjIxMS0uODkzIDEuMjExLTEuNzI2IDAtMi41LTIuMDQ5IDEuMzgyLTMuNzE1IDMuMDQ4LTUgNWE0LjkzMiA0LjkzMiAwIDAgMC0uNS0zbC00IDRhMTAxLjM0NCAxMDEuMzQ0IDAgMCAxLTE0IDE5Yy0xLjcyNi0xLjA3Ni0zLjU2LTEuMjQzLTUuNS0uNWEzNC42OTIgMzQuNjkyIDAgMCAwLTcuNSA2LjUgMjY2LjY5MSAyNjYuNjkxIDAgMCAwLTEwIDI0QzIuMjUgMzUuMjU1IDE3Ljc1IDEzLjc1NSA0OS41IDRjMjkuMTYtNS4wNjggNTEuNjYgNC43NjUgNjcuNSAyOS41IDEzLjI0MSAyOC43MjYgOC43NDEgNTQuMjI2LTEzLjUgNzYuNS05LjY4NyA3LjQyNy0yMC41MiAxMi4yNjEtMzIuNSAxNC41LTcuNTI1LTUuNjQ4LTkuODU5LTEyLjk4MS03LTIyYTgwLjAwNSA4MC4wMDUgMCAwIDAgMTQtMTYgMTA3LjMwMyAxMDcuMzAzIDAgMCAxIDktNGMuNjM1LTIuMTM1LjMwMS00LjEzNS0xLTZhNTcuMjAzIDU3LjIwMyAwIDAgMC05LjUtOC41IDEyNC42NDEgMTI0LjY0MSAwIDAgMC0xNiAyLjUgODMuMzg3IDgzLjM4NyAwIDAgMCAwLTI1Yy0xLjc4OC0uMjg1LTMuNDU1LjA0OC01IDEgMi45MDMgNy41NCAzLjQwMyAxNS4yMDcgMS41IDIzLTguMjk3LTkuOTExLTE3LjI5Ny0xMC41NzgtMjctMi0uOTUyIDMuNjE1LjM4MSA1Ljk0OCA0IDdBNjYuMTggNjYuMTggMCAwIDEgNDQuNSA5MWMtNC42NTMgNC40NC02LjE1MyA5Ljk0LTQuNSAxNi41LTIuNDY0IDMuMjk4LTUuNjMgNS42MzItOS41IDctMTEuMjA0LTcuMjUtMTkuMjA0LTE3LjA4My0yNC0yOS41QTM1OC42OTQgMzU4LjY5NCAwIDAgMSAxNiA2OS41YzIuNTU5LTMuMDMxIDUuNzI2LTUuMTk4IDkuNS02LjVhMjAuNjQ0IDIwLjY0NCAwIDAgMCA1LTdjMy45NzUuMDI1IDUuOTc1LTEuOTc1IDYtNmEzNi44OTkgMzYuODk5IDAgMCAxLTItNS41Wm01NiAxYTIuNDI4IDIuNDI4IDAgMCAxIDIgLjVjLS43NTIuNjctMS4wODYgMS41MDQtMSAyLjUtLjkwNC0uNzA5LTEuMjM3LTEuNzA5LTEtM1ptMyA3YTU0Ljk5OCA1NC45OTggMCAwIDAgNiAxMC41Yy0uNjM4IDEuNzA3LS42MzggMy41NCAwIDUuNS0yLjI5NS0zLjY4Ni00LjEyOC03LjY4Ny01LjUtMTJhOS40NjggOS40NjggMCAwIDAtMi41LTEuNWMxLjI1Ni0uNDE3IDEuOTIzLTEuMjUgMi0yLjVabS02MSAxN2MyLjk2My0yLjk3OCA2LjYzLTQuNjQ1IDExLTVsMTggOSAxMi0zYzQuNjY3IDIuNjY3IDguMzMzIDYuMzMzIDExIDExLTE0Ljc3NCAxLjUzOS0yOC40NC0xLjYyOC00MS05LjVhMTU2LjI1MyAxNTYuMjUzIDAgMCAwLTExLTIuNVptNjctMWMxLjQyNCAyLjAxNCAyLjA5IDQuMzQ4IDIgNy0uNTU4LTIuMDkzLTEuODktMy41OTMtNC00LjUgMS4yNTYtLjQxNyAxLjkyMy0xLjI1IDItMi41WiIvPjxwYXRoIHN0eWxlPSJvcGFjaXR5Oi44NzgiIGZpbGw9IiNmZWZmZmUiIGQ9Ik03NC41IDE0LjVjMi40OS0uMjAyIDQuODIzLjI5OCA3IDEuNSA0LjAzMiA1LjU1NiA5LjAzMiA3LjIyMyAxNSA1IDMuMDMgMy45ODggNC44NjQgOC40ODggNS41IDEzLjUgMi4zNjkuMjI3IDQuODY5LjM5MyA3LjUuNSAyLjY5NiA3LjA0OSAyLjM2MyAxNC4wNDktMSAyMSAyLjgxNyAzLjMyIDMuNjUxIDcuMTUzIDIuNSAxMS41YTgyLjY5NyA4Mi42OTcgMCAwIDEtNi41IDE2LjVjMS4wMjIgNi4yMS41MjIgMTIuMzc3LTEuNSAxOC41LTEuMDQ5IDEuNjA3LTIuNTQ5IDIuMjczLTQuNSAyYTE0Ny4yMzQgMTQ3LjIzNCAwIDAgMCA0LTE4LjVBMjU0LjU1NCAyNTQuNTU0IDAgMCAxIDgyIDY4LjVhMTAuNDE0IDEwLjQxNCAwIDAgMS0xLjUtNSA1NS41OSA1NS41OSAwIDAgMSAxLjUtNmMtNS0zLjY2Ny05LjMzMy04LTEzLTEzLS42NjctMS42NjctLjY2Ny0zLjMzMyAwLTVhMzEuODU3IDMxLjg1NyAwIDAgMCA0LjUtNWMtMS43OTItNS41NDYtMi4yOTItMTEuMjEyLTEuNS0xNyAuNjk4LTEuMTkgMS41MzEtMi4xOSAyLjUtM1ptMTYgMzFhMi40MjggMi40MjggMCAwIDEgMiAuNWMtLjc1Mi42Ny0xLjA4NiAxLjUwNC0xIDIuNS0uOTA0LS43MDktMS4yMzctMS43MDktMS0zWm0zIDdhNTQuOTk4IDU0Ljk5OCAwIDAgMCA2IDEwLjVjLS42MzggMS43MDctLjYzOCAzLjU0IDAgNS41LTIuMjk1LTMuNjg2LTQuMTI4LTcuNjg3LTUuNS0xMmE5LjQ2OCA5LjQ2OCAwIDAgMC0yLjUtMS41YzEuMjU2LS40MTcgMS45MjMtMS4yNSAyLTIuNVptNiAxNmMxLjQyNCAyLjAxNCAyLjA5IDQuMzQ4IDIgNy0uNTU4LTIuMDkzLTEuODktMy41OTMtNC00LjUgMS4yNTYtLjQxNyAxLjkyMy0xLjI1IDItMi41WiIvPjwvc3ZnPg=="
    },
    "5d610b86162c063cc0400125": {
        "nl": "PMD",
        "fr": "PMC",
        "en": "PMD",
        "de": "PMD",
        "image": "data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHdpZHRoPSIxMzIiIGhlaWdodD0iMTI4IiBzdHlsZT0ic2hhcGUtcmVuZGVyaW5nOmdlb21ldHJpY1ByZWNpc2lvbjt0ZXh0LXJlbmRlcmluZzpnZW9tZXRyaWNQcmVjaXNpb247aW1hZ2UtcmVuZGVyaW5nOm9wdGltaXplUXVhbGl0eTtmaWxsLXJ1bGU6ZXZlbm9kZDtjbGlwLXJ1bGU6ZXZlbm9kZDtiYWNrZ3JvdW5kOiM2MGIxZGYiPjxwYXRoIHN0eWxlPSJvcGFjaXR5Oi44NTciIGZpbGw9IiNmZWZmZmUiIGQ9Ik01NS41LS41aDI0YzI3LjY0IDYuOTczIDQ0Ljk3MyAyNC4zMDcgNTIgNTJ2MjRjLTcuMDI3IDI3LjY5My0yNC4zNiA0NS4wMjctNTIgNTJoLTI0QzE4Ljk2MiAxMTYuNDQyIDEuNzk1IDkxLjc3NSA0IDUzLjVjNi40NjYtMjguMjk4IDIzLjYzMy00Ni4yOTggNTEuNS01NFptNjIgNTFhMzI4Ljg5IDMyOC44OSAwIDAgMS0xNy0uNWMtMS43MDgtMS4wNjItMi4zNzQtMi4yMjktMi0zLjVhNTkuMjkgNTkuMjkgMCAwIDAtMTAgMy41Yy0uNTk3IDEuODg5LS45MyAzLjcyMi0xIDUuNWEyMjIuODMzIDIyMi44MzMgMCAwIDEtMTEgNC41IDMwLjEzOSAzMC4xMzkgMCAwIDAtMyAzLjUgMTI4MC45NzQgMTI4MC45NzQgMCAwIDAgMjIgNTQuNWMtMTEuNjUzIDUuOTk2LTIzLjk4NiA3Ljk5Ni0zNyA2TDcwIDEwOC41YzIuNjU2LTQuMDY3IDQuMTU2LTguMjMzIDQuNS0xMi41LTEuMjMtNS43OTItNC4yMy0xMC40NTktOS0xNCAyLjc2NS0yLjk2NiAyLjQzMi01LjYzMy0xLTgtMy4zMDQtMS4wNDItNS40Ny4xMjUtNi41IDMuNS03Ljc2OS02LjUyMi0xNS40MzUtNi41MjItMjMgMGE0MTQuMzQzIDQxNC4zNDMgMCAwIDAtMTYgMjNjLTUuNDQ4LTcuNTY0LTkuMjgxLTE1Ljg5OC0xMS41LTI1YTg3OC44MzYgODc4LjgzNiAwIDAgMSAzMS0xM2MxLjI5OS0uNTkgMi4xMzItMS41OSAyLjUtMyAxLjUwNyAxLjAzNSAzLjAwNy44NjggNC41LS41YTE0OC41MjMgMTQ4LjUyMyAwIDAgMCAxNS0yMC41Yy43MjIuNDE3IDEuMjIyIDEuMDg0IDEuNSAyIDMuMzQyLS41ODcgNi4xNzYtMi4wODcgOC41LTQuNWE3OC40MiA3OC40MiAwIDAgMS00LTExLjUgMjUuOTM2IDI1LjkzNiAwIDAgMC05IDMuNWMtLjQzLjkyLS43NjQgMS43NTMtMSAyLjVhOTUuNDUyIDk1LjQ1MiAwIDAgMC0yNi0zLjVMMjggMjkuNWMtMS4wMTEtLjgzNy0yLjE3OC0xLjE3LTMuNS0xIC4xNzEgMy4yOTctLjQ5NSAzLjYzLTIgMWEzMi4xNDUgMzIuMTQ1IDAgMCAxLTcgM0MyNC42NzggMTYuMDU2IDM4LjY3OCA2LjIyMyA1Ny41IDMgOTAuNzI2LS4xNDMgMTEzLjU2IDEzLjY5IDEyNiA0NC41YTY1LjI0MyA2NS4yNDMgMCAwIDEgMiAyNSA1OTcuNyA1OTcuNyAwIDAgMC03LjUtMThjLS44MjUtLjg4Ni0xLjgyNS0xLjIxOS0zLTFabS02MyAzMmMuNTMxIDIuMTI0IDEuODY0IDMuNjI0IDQgNC41IDEuMDc3LjQ3IDIuMDc3LjMwMyAzLS41LTEuOTkzIDUuMTA0LTQuODI2IDUuNzctOC41IDItLjczOS0yLjM4LS4yMzktNC4zOCAxLjUtNloiLz48L3N2Zz4="
    },
    "5d610b86162c063cc0400123": {
        "nl": "Papier",
        "fr": "Papier",
        "de": "Papier",
        "en": "Paper",
        "image": "data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHdpZHRoPSIxMjgiIGhlaWdodD0iMTI4IiBzdHlsZT0ic2hhcGUtcmVuZGVyaW5nOmdlb21ldHJpY1ByZWNpc2lvbjt0ZXh0LXJlbmRlcmluZzpnZW9tZXRyaWNQcmVjaXNpb247aW1hZ2UtcmVuZGVyaW5nOm9wdGltaXplUXVhbGl0eTtmaWxsLXJ1bGU6ZXZlbm9kZDtjbGlwLXJ1bGU6ZXZlbm9kZDtiYWNrZ3JvdW5kOiNmMmIwM2IiPjxwYXRoIHN0eWxlPSJvcGFjaXR5Oi44NjYiIGZpbGw9IiNmZWZmZmUiIGQ9Ik01MS41LS41aDI0YzI3LjY2NyA3IDQ1IDI0LjMzMyA1MiA1MnYyNGMtNyAyNy42NjctMjQuMzMzIDQ1LTUyIDUyaC0yNGMtMjcuNjY3LTctNDUtMjQuMzMzLTUyLTUydi0yNGM3LjAwNC0yNy42NyAyNC4zMzctNDUuMDA0IDUyLTUyWm0tMzQgODJoLTNjLTEuMjc0IDMuODgxLTMuMTA3IDcuNTQ4LTUuNSAxMS0xMS41NDItMjQuNDE0LTkuMjA4LTQ3LjQxNCA3LTY5QzQxLjEzMy0xLjI3MSA2OC45NjYtNC43NzEgOTkuNSAxM2MyMS45NDUgMTcuNDk4IDI5Ljc3OCAzOS45OTggMjMuNSA2Ny41LTExLjcwMiAzMi4wMzctMzQuNTM2IDQ2LjUzNy02OC41IDQzLjVhMTU3LjMzNCAxNTcuMzM0IDAgMCAwIDktMTguNSAxMTk5LjgzNSAxMTk5LjgzNSAwIDAgMS0zMy04LjVjLTEuMTIyLTMuNDA5LTEuMjg5LTYuOTA5LS41LTEwLjVhMTY4LjE5IDE2OC4xOSAwIDAgMSAxLjUgOCA1OTguMzI1IDU5OC4zMjUgMCAwIDEgNDEuNSAxM2MtLjU1LTQuNjA1LTEuMDUtOS4yNzEtMS41LTE0YTc2Ljk0IDc2Ljk0IDAgMCAwIDEwLTEgNDguODYgNDguODYgMCAwIDAtNi0xMy41IDc5LjkxNSA3OS45MTUgMCAwIDAtMTEgMSAzNS4yNjYgMzUuMjY2IDAgMCAwIDMtMTAuNSA1NDcwOS43IDU0NzA5LjcgMCAwIDEtNDItMTMgNDkuMjg1IDQ5LjI4NSAwIDAgMS0yIDExbC0xMCAxYTEwMi4zNDMgMTAyLjM0MyAwIDAgMCA0IDEzWm01Ni01M2MtMy41MjcgMS4zNTItNi42OTMgMy4zNTItOS41IDYtLjY4NC0xLjI4NC0uNTE3LTIuNDUuNS0zLjVhNDUuNzg1IDQ1Ljc4NSAwIDAgMSA5LTIuNVptLTU2IDUzYzIuMjE3Ljg2OSA0LjU1IDEuMjAyIDcgMS0yLjEgMS4xMTItNC40MzMgMS43NzgtNyAydi0zWm03IDFjMS41MzUtMS4yODggMy4yMDEtMS4yODggNSAwLS4xMjQuNjA3LS40NTcuOTQtMSAxLTEuMDY4LS45MzQtMi40MDEtMS4yNjgtNC0xWiIvPjxwYXRoIHN0eWxlPSJvcGFjaXR5Oi45MzQiIGZpbGw9IiNmZWZmZmUiIGQ9Ik02OC41IDIwLjVhMzMyMS43OCAzMzIxLjc4IDAgMCAwIDExLThsOC41IDExYTI0MS4xMjMgMjQxLjEyMyAwIDAgMSAxMS41LTUgMTM3MS4xODkgMTM3MS4xODkgMCAwIDEgMTkgNDcuNWMtLjk0NCAxLjQ3Ny0yLjI3NyAyLjQ3Ny00IDNhMTc2Mi44MDcgMTc2Mi44MDcgMCAwIDAtMzEgMTIuNSA5NTguMTE4IDk1OC4xMTggMCAwIDEtMTQtMzIgNzguODUzIDc4Ljg1MyAwIDAgMCA2IDE5bC0xIDFhNjk2LjQxIDY5Ni40MSAwIDAgMS0zNy0yNSA4MjAuNzIgODIwLjcyIDAgMCAxIDIxLjUtMzJjMy41ODcgMi4zNDcgNi43NTQgNS4wMTMgOS41IDhabTUgOGE0NS43ODUgNDUuNzg1IDAgMCAwLTkgMi41Yy0xLjAxNyAxLjA1LTEuMTg0IDIuMjE2LS41IDMuNSAyLjgwNy0yLjY0OCA1Ljk3My00LjY0OCA5LjUtNloiLz48L3N2Zz4="
    },
    "5d610b86162c063cc0400112": {
        "nl": "Restafval zak",
        "fr": "Déchets non recyclables sac",
        "de": "Restabfall tasche",
        "en": "Non-recyclable waste bag",
        "image": "data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHdpZHRoPSIxMjgiIGhlaWdodD0iMTI4IiBzdHlsZT0ic2hhcGUtcmVuZGVyaW5nOmdlb21ldHJpY1ByZWNpc2lvbjt0ZXh0LXJlbmRlcmluZzpnZW9tZXRyaWNQcmVjaXNpb247aW1hZ2UtcmVuZGVyaW5nOm9wdGltaXplUXVhbGl0eTtmaWxsLXJ1bGU6ZXZlbm9kZDtjbGlwLXJ1bGU6ZXZlbm9kZCI+PHBhdGggc3R5bGU9Im9wYWNpdHk6MSIgZmlsbD0iIzc3NyIgZD0iTS0uNS0uNWg1M2MtMjcuOTcgNy4zMDMtNDUuNjM2IDI0Ljk3LTUzIDUzdi01M1pNNzMuNS0uNWg1NHY1M2MtNy40MzktMjguNDM5LTI1LjQzOS00Ni4xMDYtNTQtNTNaIi8+PHBhdGggc3R5bGU9Im9wYWNpdHk6MSIgZmlsbD0iI2ZiZmJmYiIgZD0iTTUyLjUtLjVoMjFjMjguNTYxIDYuODk0IDQ2LjU2MSAyNC41NjEgNTQgNTN2MjFjLTcuMzUyIDMwLjM1NC0yNi4zNTIgNDguMzU0LTU3IDU0aC0xOGMtMjguNDA0LTcuNDA1LTQ2LjA3LTI1LjQwNS01My01NHYtMjFjNy4zNjQtMjguMDMgMjUuMDMtNDUuNjk3IDUzLTUzWiIvPjxwYXRoIHN0eWxlPSJvcGFjaXR5OjEiIGZpbGw9IiM3NzciIGQ9Ik01NC41IDEuNWMzNy43NTQtMS4wNTggNjEuMjU0IDE2LjYwOSA3MC41IDUzIDEuNzMyIDE5LjQyOS0zLjc2OCAzNi40MjktMTYuNSA1MWwtMS00LjVhNTAuODg0IDUwLjg4NCAwIDAgMCAxLjUtMTYuNUMxMDQuNTA0IDczLjAxMyA5OC4wMDQgNjIuODQ3IDg5LjUgNTRsLTE4LTQuNXYtNmM3LjQ5NS40NjQgMTMuNDk1LTIuMjAzIDE4LThhNDMuMDc5IDQzLjA3OSAwIDAgMC0xLjUtNUExMTkuOTQ4IDExOS45NDggMCAwIDEgNzUuNSAxN2MtNi4zMTctLjU0LTEyLjQ4NC0xLjA0LTE4LjUtMS41YTQwLjc3OCA0MC43NzggMCAwIDAtNS41IDIuNWMzLjcxMiA1LjI1OCA1Ljg4IDExLjA5MiA2LjUgMTcuNSAxMC4xNjQgMTAuODMgNy42NjQgMTUuMzMtNy41IDEzLjUtOS41OTQgMS44LTE3LjkyNyA1Ljk2Ni0yNSAxMi41YTE0Ni42MDkgMTQ2LjYwOSAwIDAgMC0xMiAzOEMtNS45OSA2Ny4zMS0xLjY1NiAzOC44MSAyNi41IDE0YzguNTYxLTYuMTE4IDE3Ljg5NS0xMC4yODUgMjgtMTIuNVoiLz48cGF0aCBzdHlsZT0ib3BhY2l0eToxIiBmaWxsPSIjN2U3ZTdlIiBkPSJNNTcuNSA1Mi41YzQuMzM1LjQxNyA4LjY2OC45MTcgMTMgMS41YTI0Ni44NSAyNDYuODUgMCAwIDAgMTkgOWM5Ljg1IDExLjk5IDkuMTgyIDEyLjk5LTIgM2ExNDAuNTIyIDE0MC41MjIgMCAwIDEtMTQtNy41bC0xIDFhNDEuMSA0MS4xIDAgMCAxIDEuNSAxNyAxMDEuMTgzIDEwMS4xODMgMCAwIDAtOC41LTE3IDE0Ljk3NCAxNC45NzQgMCAwIDAtMy41IDMgMTIxLjQzNiAxMjEuNDM2IDAgMCAxLTcgMTNjLS40OC00LjEwNS4wMi04LjEwNSAxLjUtMTJhNC40NTIgNC40NTIgMCAwIDAtMi0xLjVsNS01YTEzNS45NDkgMTM1Ljk0OSAwIDAgMC0xNSA2IDI1Mi4yMTggMjUyLjIxOCAwIDAgMC0xMSAxNS41YzEuMDA1LTUuODE0IDMuMTcyLTExLjQ4MSA2LjUtMTdhNDM2LjY3OCA0MzYuNjc4IDAgMCAxIDE3LjUtOVoiLz48cGF0aCBzdHlsZT0ib3BhY2l0eToxIiBmaWxsPSIjNzc3IiBkPSJNLS41IDczLjVjNi45MyAyOC41OTUgMjQuNTk2IDQ2LjU5NSA1MyA1NGgtNTN2LTU0Wk0xMjcuNSA3My41djU0aC01N2MzMC42NDgtNS42NDYgNDkuNjQ4LTIzLjY0NiA1Ny01NFoiLz48L3N2Zz4="
    },
    "5d610b86162c063cc0400127": {
        "nl": "Snoeiafval",
        "fr": "Résidus de taille",
        "de": "Schneideabfälle",
        "en": "Pruning waste",
        "image": "data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHdpZHRoPSIxMjgiIGhlaWdodD0iMTI4IiBzdHlsZT0iYmFja2dyb3VuZDojNjM4OTE5O3NoYXBlLXJlbmRlcmluZzpnZW9tZXRyaWNQcmVjaXNpb247dGV4dC1yZW5kZXJpbmc6Z2VvbWV0cmljUHJlY2lzaW9uO2ltYWdlLXJlbmRlcmluZzpvcHRpbWl6ZVF1YWxpdHk7ZmlsbC1ydWxlOmV2ZW5vZGQ7Y2xpcC1ydWxlOmV2ZW5vZGQiPjxwYXRoIHN0eWxlPSJvcGFjaXR5Oi44NDciIGZpbGw9IiNmZWZmZmUiIGQ9Ik01MS41LS41aDI0YzI3LjY2NyA3IDQ1IDI0LjMzMyA1MiA1MnYyNGMtNy4wMDQgMjcuNjcxLTI0LjMzNyA0NS4wMDQtNTIgNTJoLTI0Yy0yNy42NjctNy00NS0yNC4zMzMtNTItNTJ2LTI0YzctMjcuNjY3IDI0LjMzMy00NSA1Mi01MlptMjMgNzJhMTQ3LjkxOSAxNDcuOTE5IDAgMCAxIDYuNS0zMSAxNi4yNSAxNi4yNSAwIDAgMCAwLTggMzU2Ljg3MiAzNTYuODcyIDAgMCAwLTUuNS0xNGMtMy45NDYtLjY4NC03Ljk0Ni0uNjg0LTEyIDBhMjUuOTM2IDI1LjkzNiAwIDAgMCAzLjUgOSAzNi41NCAzNi41NCAwIDAgMSAxLjUgOS41IDQwNC41NjUgNDA0LjU2NSAwIDAgMS05IDQ0LjVjLTEuMTUgMS4yMzEtMi4zMTcgMS4yMzEtMy41IDBsLTUtMTRhMzguOSAzOC45IDAgMCAwLTUuNS01YzYuNjEyLTYuNzEgOC43NzktMTQuNzEgNi41LTI0YTQ0Ljc1NyA0NC43NTcgMCAwIDAtNi41LTE0Yy0xMC43MTkgMTAuMTA5LTEyLjcxOSAyMS43NzUtNiAzNWwtMS41IDFBMzcuMTU1IDM3LjE1NSAwIDAgMCAyNS41IDU5Yy0xLjUzNiAxLjYtMi4wMzYgMy40MzMtMS41IDUuNSA3LjA4My0uNTggMTMuOTE3LjkyIDIwLjUgNC41IDguMjE1IDkuMzQ5IDYuNTQ5IDExLjg0OS01IDcuNS0xMC40NyAyLjE2My0xOC44MDQgNy40OTYtMjUgMTZhNC45MzggNC45MzggMCAwIDAgMSAyLjVjMTEuMzIgMy43MTYgMjEuOTg2IDIuMzgzIDMyLTRhMzUuOTQgMzUuOTQgMCAwIDAgMy41LTQuNWwzIDNhMTYxLjM2IDE2MS4zNiAwIDAgMS0xLjUgMzVDMTMuMjQyIDExMy4wMDItMi45MjUgODcuMDAyIDQgNDYuNWM5Ljk0Ni0yOC4yNjYgMjkuOTQ2LTQzLjI2NiA2MC00NSA0MC4zOSA0LjcyMSA2MC43MjMgMjcuMzg4IDYxIDY4LTQuNDk0IDI5LjY2LTIxLjMyNyA0Ny45OTQtNTAuNSA1NWEzMzguMDY1IDMzOC4wNjUgMCAwIDEtLjUtNDVMODcuNSA2OGMxNi4yNDItMy43MzggMjQuNTc2LTEzLjkwNCAyNS0zMC41LTE2LjEyNiAxLjI5My0yNS4yOTMgOS45Ni0yNy41IDI2YTExNC4xNTkgMTE0LjE1OSAwIDAgMS0xMC41IDhaIi8+PC9zdmc+"
    },
    "5d610b86162c063cc0400133": {
        "nl": "Restafval",
        "fr": "Déchets non recyclables",
        "de": "Restabfall",
        "en": "Non-recyclable waste",
        "image": "data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHdpZHRoPSIxMjgiIGhlaWdodD0iMTI4IiBzdHlsZT0ic2hhcGUtcmVuZGVyaW5nOmdlb21ldHJpY1ByZWNpc2lvbjt0ZXh0LXJlbmRlcmluZzpnZW9tZXRyaWNQcmVjaXNpb247aW1hZ2UtcmVuZGVyaW5nOm9wdGltaXplUXVhbGl0eTtmaWxsLXJ1bGU6ZXZlbm9kZDtjbGlwLXJ1bGU6ZXZlbm9kZDtiYWNrZ3JvdW5kOiM2MDgyODIiPjxwYXRoIHN0eWxlPSJvcGFjaXR5Oi44NDMiIGZpbGw9IiNmZWZmZmUiIGQ9Ik01MS41LS41aDI0YzI3LjY2NyA3IDQ1IDI0LjMzMyA1MiA1MnYyNGMtNyAyNy42NjctMjQuMzMzIDQ1LTUyIDUyaC0yNGMtMjcuNjY3LTctNDUtMjQuMzMzLTUyLTUydi0yNGM3LTI3LjY2NyAyNC4zMzMtNDUgNTItNTJabTcgODJjMS4zMzMtLjMzMyAxLjMzMy0uNjY3IDAtMWE3NDEuODMzIDc0MS44MzMgMCAwIDAgNy0yMC41YzkuNjYtLjUgMTkuMzI4LS42NjYgMjktLjUuMjEzLTEuNjQ0LS4xMi0zLjE0NC0xLTQuNUE1MTkuMTY3IDUxOS4xNjcgMCAwIDAgNDggMzguNWMtNSAuMzI4LTguNjY3IDIuNjYyLTExIDdhNjk5LjU2MiA2OTkuNTYyIDAgMCAxLTcuNSAyNSA2MzAuNTgxIDYzMC41ODEgMCAwIDAgMjYgMTAgOTYxLjY4NiA5NjEuNjg2IDAgMCAxLTI3LTUgMTA1NC4yNzMgMTA1NC4yNzMgMCAwIDEgMi41IDQwQzUuNTYgOTcuMTgzLTIuNzczIDcyLjg1IDYgNDIuNWMxMC43NjgtMjUuMzA4IDI5LjkzNS0zOC42NDIgNTcuNS00MCAzMy43MTMgMi4yMTQgNTMuODggMTkuODggNjAuNSA1MyAyLjI2OSAyMi44ODUtNS4zOTggNDEuNTUxLTIzIDU2IC44MjktNy42MzQgMS45OTYtMTUuMyAzLjUtMjNhNC45MzIgNC45MzIgMCAwIDAtMS0yLjUgMjg5LjIzNiAyODkuMjM2IDAgMCAwLTM0IDAgNC45MzggNC45MzggMCAwIDAtMSAyLjUgNTM0LjUyMyA1MzQuNTIzIDAgMCAwIDcgMzQuNSAyOC4wNCAyOC4wNCAwIDAgMC01IDEuNSA3ODUuOTI2IDc4NS45MjYgMCAwIDEtMTItNDNabS0xMyAxNGE0MTIuNDkzIDQxMi40OTMgMCAwIDEgMTggMjhjLTguNSAxLjE5NC0xNi41LS4zMDYtMjQtNC41YTEzNC45OTggMTM0Ljk5OCAwIDAgMCA2LTIzLjVaIi8+PHBhdGggc3R5bGU9Im9wYWNpdHk6Ljg5NyIgZmlsbD0iI2ZlZmZmZSIgZD0iTTYyLjUgMTYuNWM5Ljc4Ljk1OCAxMy42MTQgNi4yOTEgMTEuNSAxNi01LjM3MiA2Ljk0NS0xMS4zNzIgNy42MTItMTggMi00LjI3Ny04LjQzLTIuMTEtMTQuNDMgNi41LTE4WiIvPjxwYXRoIHN0eWxlPSJvcGFjaXR5Oi45MjciIGZpbGw9IiNmZWZmZmUiIGQ9Ik01OC41IDgwLjVoLTNhNjMwLjU4MSA2MzAuNTgxIDAgMCAxLTI2LTEwIDY5OS41NjIgNjk5LjU2MiAwIDAgMCA3LjUtMjVjMi4zMzMtNC4zMzggNi02LjY3MiAxMS03QTUxOS4xNjcgNTE5LjE2NyAwIDAgMSA5My41IDU1Yy44OCAxLjM1NiAxLjIxMyAyLjg1NiAxIDQuNS05LjY3Mi0uMTY2LTE5LjM0IDAtMjkgLjVhNzQxLjgzMyA3NDEuODMzIDAgMCAxLTcgMjAuNVoiLz48cGF0aCBzdHlsZT0ib3BhY2l0eTouODMyIiBmaWxsPSIjZmVmZmZlIiBkPSJNODUuNSA2Ni41YzMuNTg1LS4yMzEgNi43NTIuNzY5IDkuNSAzIDEuMDc5IDMuODA1LjQxMiA3LjEzOC0yIDEwYTE4LjA4OCAxOC4wODggMCAwIDAtMy41LTJjLTMuNjI3IDEuNTc1LTYuNzkzLjkwOC05LjUtMi0uNjk5LTIuODIyLjQ2OC00LjQ4OCAzLjUtNSAuODYyLTEuMjY2IDEuNTMtMi42IDItNFoiLz48L3N2Zz4="
    }
}
