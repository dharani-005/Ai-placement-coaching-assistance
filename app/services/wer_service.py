import numpy as np
class WERService:

    def calculate_wer(self, reference, hypothesis):

        ref_words = reference.lower().split()
        hyp_words = hypothesis.lower().split()

        r = len(ref_words)
        h = len(hyp_words)

        d = np.zeros((r+1)*(h+1), dtype=np.uint8)
        d = d.reshape((r+1, h+1))

        for i in range(r+1):
            d[i][0] = i
        for j in range(h+1):
            d[0][j] = j

        for i in range(1, r+1):
            for j in range(1, h+1):

                if ref_words[i-1] == hyp_words[j-1]:
                    cost = 0
                else:
                    cost = 1

                d[i][j] = min(
                    d[i-1][j] + 1,
                    d[i][j-1] + 1,
                    d[i-1][j-1] + cost
                )

        wer = d[r][h] / float(r)

        return round(wer, 3)