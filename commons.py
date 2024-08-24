QUERY_SMART_CONTRACT_API_URI = 'https://testapi.qubic.org/v1/querySmartContract'

HEADERS = {
    'accept': 'application/json',
    'Content-Type': 'application/json',
}

QTRY_CONTRACT_INDEX = 2

def make_json_data(contract_index: int, input_type: int, input_size: int, request_data: str):
    return {
        'contractIndex': contract_index,
        'inputType': input_type,
        'inputSize': input_size,
        'requestData': request_data,
    }
