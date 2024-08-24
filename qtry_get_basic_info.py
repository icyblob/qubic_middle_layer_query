import struct
import requests
import base64
import commons


def get_basic_info():
    json_data = commons.make_json_data(commons.QTRY_CONTRACT_INDEX, 1, 0, "")

    response = requests.post(commons.QUERY_SMART_CONTRACT_API_URI, headers=commons.HEADERS, json=json_data)
    data = base64.b64decode(response.json()['responseData'])

    unpacked_data = struct.unpack('<5Q I 4x 9Q 32s', data)

    (
        fee_per_slot_per_hour,
        game_operator_fee,
        shareholder_fee,
        min_bet_slot_amount,
        burn_fee,
        n_issued_bet,
        money_flow,
        money_flow_through_issue_bet,
        money_flow_through_join_bet,
        money_flow_through_finalize_bet,
        earned_amount_for_shareholder,
        paid_amount_for_shareholder,
        earned_amount_for_bet_winner,
        distributed_amount,
        burned_amount,
        game_operator_bytes,
    ) = unpacked_data
    game_operator = base64.b32encode(game_operator_bytes).decode('ascii')

    print("feePerSlotPerHour:", fee_per_slot_per_hour)
    print("gameOperatorFee:", game_operator_fee)
    print("shareholderFee:", shareholder_fee)
    print("minBetSlotAmount:", min_bet_slot_amount)
    print("burnFee:", burn_fee)
    print("nIssuedBet:", n_issued_bet)
    print("moneyFlow:", money_flow)
    print("moneyFlowThroughIssueBet:", money_flow_through_issue_bet)
    print("moneyFlowThroughJoinBet:", money_flow_through_join_bet)
    print("moneyFlowThroughFinalizeBet:", money_flow_through_finalize_bet)
    print("earnedAmountForShareHolder:", earned_amount_for_shareholder)
    print("paidAmountForShareHolder:", paid_amount_for_shareholder)
    print("earnedAmountForBetWinner:", earned_amount_for_bet_winner)
    print("distributedAmount:", distributed_amount)
    print("burnedAmount:", burned_amount)
    print("gameOperator:", game_operator) # This one is currently wrong !!!!!!! [TODO]: Make it right


if __name__ == "__main__":
    get_basic_info()
