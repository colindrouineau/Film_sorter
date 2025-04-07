import utils as u

PUNCTUATION = [
    " ",
    "'",
    "&",
    "~",
    "#",
    "{",
    "(",
    "[",
    "-",
    "|",
    "`",
    "_",
    ")",
    "°",
    "]",
    "=",
    "+",
    "}",
    "<",
    ">",
    ",",
    "?",
    ";",
    ".",
    ":",
    "!",
    "§",
]


STOP_WORDS_ENGLISH = "m, re, s, ve, a, about, above, after, against, all, am, and, an, another, any, are, around, as, at, be, because, been, before, being, below, between, both, but, by, can, could, did, do, does, doing, down, during, each, either, for, from, further, had, has, have, having, he, her, here, hers, herself, him, himself, his, how, i, if, in, inside, into, is, it, its, itself, me, more, most, much, my, myself, neither, no, nor, not, of, off, on, once, only, or, other, ought, our, ours, ourselves, out, outside, over, own, same, shan't, she, should, so, some, such, than, that, the, their, theirs, them, themselves, then, there, these, they, this, those, though, through, to, too, under, until, up, upon, us, used, very, was, we, were, what, when, where, which, while, who, whom, whose, why, with, within, without, would, you, your, yours, yourself, yourselves"
STOP_WORDS_FRENCH = "a, ai, aie, aies, ait, après, as, auquel, avant, avec, avais, avaient, avions, aura, aurai, auras, aurait, aurions, aurons, auraient, aurez, auriez, aurons, ayez, ayons, bien, mais, malgré, me, moins, moi, mon, ma, mes, ni, nous, on, ou, par, parce, pas, pendant, pour, sans, se, sous, soient, soit, sois, soyez, soyons, suis, sur, te, ton, ta, tes, toi, ton, ta, tes, tout, toute, toutes, un, une, vos, votre, vous, à, ça, ce, cet, celle, celles, ceux, chez, chacun, chacune, dans, de, des, du, dont, elle, elles, en, es, est, et, été, étions, étiez, été, être, fûmes, fûtes, furent, fut, fus, il, ils, jusque, la, le, les, leur, leurs, lui, mais, malgré, me, mes, moi, mon, nôtre, nôtres, notre, nous, on, ou, par, parce, pas, pendant, pour, sans, se, sous, soient, soit, sois, soyez, soyons, suis, sur, te, ton, ta, tes, toi, ton, ta, tes, tout, toute, toutes, un, une, vos, votre, vous, étaient, étais, étions, étiez, été, être, fus, fut, fûmes, fûtes, furent, serai, seras, sera, serons, serez, seront, serais, serait, serions, seriez, seraient, sois, soit, soyons, soyez, soient, ai, as, a, avons, avez, ont, avais, avait, avions, aviez, avaient, eus, eut, eûmes, eûtes, eurent, aurai, auras, aura, aurons, aurez, auront, aurais, aurait, aurions, auriez, auraient, aie, aies, ait, ayons, ayez, aient, mais, ou, et, donc, or, ni, car, que, dont, où, quand, comme, si, lorsque, puisque, quoique, bien, pour, afin, parce, de, peur, moins, condition, à, après, avant, avec, chez, contre, dans, dès, en, entre, hors, jusque, malgré, par, pendant, sans, sous, sur, vers, le, un, des, du"
STOP_WORDS_ENGLISH = STOP_WORDS_ENGLISH.split(", ")
STOP_WORDS_FRENCH = STOP_WORDS_FRENCH.split(", ")


if __name__ == "__main__":
    print(STOP_WORDS_FRENCH)
    print(STOP_WORDS_ENGLISH)
