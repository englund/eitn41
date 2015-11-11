import argparse

def get_check_digit(card_nbr):
    nbr = card_nbr[:-1]
    nbr = nbr[::-1]

    sum_digits = ""
    for i, d in enumerate(nbr):
        if (i % 2) == 0:
            d = int(d)
            d = d * 2
            if d > 9:
                d = (d % 10) + 1
            sum_digits += str(d)
        else:
            sum_digits += d

    validation = 0
    for d in sum_digits:
        validation += int(d)
    check_digit = validation * 9 % 10

    return check_digit

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Validate credit card numbers.')
    parser.add_argument('-c', '--card', dest='card_nbr',
            help='credit card number')
    args = parser.parse_args()

    check_digit = get_check_digit(args.card_nbr)
    x =  int(args.card_nbr[-1:])

    if check_digit == x:
        print "valid card number", args.card_nbr
    else:
        print "invalid card number, check digit should be %s but is %s" % (check_digit, x)
