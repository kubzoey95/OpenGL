import json
import pprint
import cw1.zad12, cw1.zad3, cw1.zad4, cw1.zad5, cw1.zad6, cw1.zad78
import cw2.zad0, cw2.zad01, cw2.zad02, cw2.zad1, cw2.zad2, cw2.zad3, cw2.zad4

zads_dict = {
    'cw1': {
        'zad12': cw1.zad12.main,
        'zad3': cw1.zad3.main,
        'zad4': cw1.zad4.main,
        'zad5': cw1.zad5.main,
        'zad6': cw1.zad6.main,
        'zad78': cw1.zad78.main
    },
    'cw2': {
        'zad0': cw2.zad0.main,
        'zad01': cw2.zad01.main,
        'zad02': cw2.zad02.main,
        'zad1': cw2.zad1.main,
        'zad2': cw2.zad2.main,
        'zad3': cw2.zad3.main,
        'zad4': cw2.zad4.main
    }
}

pprint.pprint(zads_dict)

inp = input('prosze wybrac zadanie ze slownika powyzej na przyklad: ["cw1", "zad12"] (cudzyslowy sa "wazne")\n')

print(inp)

inp = json.loads(inp)

zads_dict[inp[0]][inp[1]]()
