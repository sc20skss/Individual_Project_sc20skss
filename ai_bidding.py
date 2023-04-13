
def bidding_heuristic(hand):
    spades_count = 0
    high_cards_count = 0
    prob_win = {
        'A' : 0.9, 'K' : 0.8, 'Q' : 0.7, 'J' : 0.6, '10' : 0.5
    }
    rest = []
    for card in hand:
        if card.suite == '♠':
            spades_count += 1
        if card.order in ["A", "K", "Q", "J"]:
            high_cards_count += prob_win[card.order]
        else:
            rest.append(card)
    
    def card_value(card_order):
        if card_order == 'A': return 0.9
        elif card_order == 'K': return 0.8
        elif card_order == 'Q': return 0.7 
        elif card_order == 'J': return 0.6
        return (int(card_order) - 1) / 20

    # Estimate the probability of winning at least n tricks based on the number of spades and high cards
    def can_win(n, rest):
        win_value = high_cards_count
        for card in rest:
            if card.suite == '♠':
                win_value += 0.4 * card_value(card.order)
        
        return win_value > n
    
    # Bid the number of tricks with the highest estimated probability of winning
    best_bid = 1
    for i in range(1, 10):
        probability = can_win(i, rest)
        if probability == False:  break
        else:
            best_bid = i 
    return best_bid

def bidding_greedy(hand):
    spade_count = 0
    higher_card_count = 0
    suite_count = [0, 0, 0, 0] # spade, heart, diamond, clubs
    suite_id = {'♠' : 0, '♥' : 1, '♦' : 2, '♣' : 3}
    for card in hand:
        if card.suite == '♠': spade_count += 1
        if card.suite == '♠': suite_count[0] += 1
        elif card.suite == '♥': suite_count[1] += 1
        elif card.suite == '♦': suite_count[2] += 1
        else: suite_count[3] += 1


    for card in hand:
        if card.order in ['A', 'K']: higher_card_count += 1
        elif card.order == 'Q' and suite_count[suite_id[card.suite]] <= 3: higher_card_count += 1

    print(suite_count, spade_count, higher_card_count)
    bid = higher_card_count
    temp_spade_count = spade_count
    for each_count in suite_count:
        if each_count < 2 and temp_spade_count > 0: 
            bid += 1
            temp_spade_count -= 1
    
    return bid
