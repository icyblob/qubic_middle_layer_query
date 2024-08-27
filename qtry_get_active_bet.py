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
    active_bet_ids = unpacked_data[1: 1 + count]

    print(f"Active Bet Count: {count}")
    print("Active Bet IDs:", active_bet_ids)

    return count, active_bet_ids


def get_bet_detail(bet_id):
    bet_id_bytes = struct.pack('<I', bet_id)
    input_base64 = base64.b64encode(bet_id_bytes).decode('ascii')

    json_data = commons.make_json_data(commons.QTRY_CONTRACT_INDEX, 2, 4, input_base64)

    response = requests.post(
        commons.QUERY_SMART_CONTRACT_API_URI,
        headers=commons.HEADERS,
        json=json_data
    )

    data = base64.b64decode(response.json()['responseData'])
    print('Response size:', len(data))

    '''
        struct getBetInfo_output {
        // meta data info
        uint32 betId;
        uint32 nOption;      // options number
        id creator;
        id betDesc;      // 32 bytes 
        id_8 optionDesc;  // 8x(32)=256bytes
        id_8 oracleProviderId; // 256x8=2048bytes
        uint32_8 oracleFees;   // 4x8 = 32 bytes

        uint32 openDate;     // creation date, start to receive bet
        uint32 closeDate;    // stop receiving bet date
        uint32 endDate;       // result date
        // Amounts and numbers
        uint64 minBetAmount;
        uint32 maxBetSlotPerOption;
        uint32_8 currentBetState; // how many bet slots have been filled on each option
        sint8_8 betResultWonOption;
        sint8_8 betResultOPId;
    };
    '''
    output_struct_format = (
        '<'  # Little-endian
        'I'  # uint32 betId (4 bytes)
        'I'  # uint32 nOption (4 bytes)
        '32s'  # id creator (32 bytes)
        '32s'  # id betDesc (32 bytes)
        '256s'  # id_8 optionDesc (8 * 32 bytes = 256 bytes)
        '256s'  # id_8 oracleProviderId (8 * 32 bytes = 256 bytes)
        '8I'  # uint32_8 oracleFees (8 * 4 bytes = 32 bytes)
        'I'  # uint32 openDate (4 bytes)
        'I'  # uint32 closeDate (4 bytes)
        'I'  # uint32 endDate (4 bytes)
        '4x'  # Padding for alignment (4 byte)
        'Q'  # uint64 minBetAmount (8 bytes)
        'I'  # uint32 maxBetSlotPerOption (4 bytes)
        '4x'  # Padding for alignment (4 byte)
        '8I'  # uint32_8 currentBetState (8 * 4 bytes = 32 bytes)
        '8b'  # sint8_8 betResultWonOption (8 * 1 byte = 8 bytes)
        '8b'  # sint8_8 betResultOPId (8 * 1 byte = 8 bytes)
    )

    unpacked_data = struct.unpack(output_struct_format, data)

    bet_id = unpacked_data[0]
    n_option = unpacked_data[1]
    creator = unpacked_data[2]
    bet_desc = unpacked_data[3]
    option_desc = unpacked_data[4]
    oracle_provider_id = unpacked_data[5]
    oracle_fees = unpacked_data[6:14]  # uint32_8 oracleFees
    open_date = unpacked_data[14]
    close_date = unpacked_data[15]
    end_date = unpacked_data[16]
    min_bet_amount = unpacked_data[17]
    max_bet_slot_per_option = unpacked_data[18]
    current_bet_state = unpacked_data[19:27]  # uint32_8 currentBetState
    bet_result_won_option = unpacked_data[27:35]  # sint8_8 betResultWonOption
    bet_result_op_id = unpacked_data[35:43]  # sint8_8 betResultOPId

    print("betId:", bet_id)
    print("nOption:", n_option)
    print("creator:", creator)
    print("betDesc:", bet_desc)
    print("optionDesc:", option_desc)
    print("oracleProviderId:", oracle_provider_id)
    print("oracleFees:", oracle_fees)
    print("openDate:", open_date)
    print("closeDate:", close_date)
    print("endDate:", end_date)
    print("minBetAmount:", min_bet_amount)
    print("maxBetSlotPerOption:", max_bet_slot_per_option)
    print("currentBetState:", current_bet_state)
    print("betResultWonOption:", bet_result_won_option)
    print("betResultOPId:", bet_result_op_id)


if __name__ == "__main__":
    bet_count, all_active_bet_ids = get_active_bet()
    [get_bet_detail(id_) for id_ in all_active_bet_ids]
