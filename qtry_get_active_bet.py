import struct
import requests
import base64
import commons


def get_active_bet():
    json_data = commons.make_json_data(commons.QTRY_CONTRACT_INDEX, 4, 0, "")

    response = requests.post(
        commons.QUERY_SMART_CONTRACT_API_URI, headers=commons.HEADERS, json=json_data)
    data = base64.b64decode(response.json()['responseData'])

    unpacked_data = struct.unpack('<I1024I', data)

    count = unpacked_data[0]
    active_bet_ids = unpacked_data[1 : 1 + count]

    print(f"Active Bet Count: {count}")
    print("Active Bet IDs:", active_bet_ids)

    return count, active_bet_ids


if __name__ == "__main__":
    get_active_bet()
