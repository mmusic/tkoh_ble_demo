SERVER_IP = '143.89.49.63'
TCP_PORT = 5000
FLASK_PORT = 8080
INTERNAL_REQUEST_USERNAME = 'MTR_SERVICE'
INTERNAL_REQUEST_PSW = 'MTREC2021'
DB_CONNECT_INFO = {'db_usr': 'postgres',
                   'db_usr_psw': 'mtrec2020',
                   'db_host': SERVER_IP,
                   'db_port': '7023',
                   'db_name': 'tkoh_cms'}
CACHE_ADDR = ('localhost', 6000)


MAPS = {
    11:[[12706277.690103108,2481623.246629678,1],[12706284.535684245,2481617.0470793806,1],[12706281.419510113,2481613.567757178,1],[12706274.510153892,2481619.889362369,1]],
    12:[[12706273.220346142,2481624.739446419,1],[12706276.38680139,2481621.9106907123,1],[12706274.58212394,2481619.9376261393,1],[12706271.416573979,2481622.718398687,1]],
    13:[[12706271.487353643,2481622.7337906747,1],[12706273.282278039,2481621.1039976254,1],[12706269.326858638,2481616.9680480147,1],[12706267.622451758,2481618.434217962,1]],
    14:[[12706267.63500547,2481618.463439361,1],[12706270.666027356,2481615.598304704,1],[12706268.442569843,2481613.272768055,1],[12706265.345961632,2481615.9447070155,1]],
    15:[[12706235.556680152,2481604.2035290315,1],[12706241.60767543,2481599.9781230814,1],[12706230.478126813,2481587.84979271,1],[12706225.064659016,2481592.6859295224,1]],
    16:[[12706235.494944159,2481604.2570478534,1],[12706247.7252712,2481614.42667308,1],[12706251.581759445,2481611.354846987,1],[12706240.82410425,2481599.3095443593,1]],
    17:[[12706255.200088443,2481623.0361075033,1],[12706258.087044554,2481620.46363867,1],[12706250.125492722,2481612.034188571,1],[12706247.235101229,2481614.2903745444,1]],
    18:[[12706258.09952207,2481620.326320182,1],[12706267.117520342,2481611.9477142035,1],[12706264.410834756,2481610.045303761,1],[12706255.690944975,2481618.062382567,1]],
    19:[[12706266.824782902,2481615.621133733,1],[12706264.905821137,2481613.6741257287,1],[12706267.272209052,2481611.8907338833,1],[12706269.350359378,2481614.1603339445,1]],

    21:[[12706228.033743076,2481650.5781811867,2],[12706234.78375774,2481644.7008796954,2],[12706229.280943988,2481637.9260257455,2],[12706222.404175356,2481643.840154998,2]],
    22:[[12706234.866305113,2481644.779956806,2],[12706243.788736084,2481637.3439769014,2],[12706237.89979419,2481630.9904778367,2],[12706229.070176095,2481637.9614944565,2]],
    23:[[12706243.744529262,2481637.4598792526,2],[12706253.393543372,2481629.374802574,2],[12706249.07740188,2481624.2906050193,2],[12706239.255960654,2481632.606132634,2]],
    24:[[12706239.129206706,2481632.642957963,2],[12706241.646477466,2481630.6233843733,2],[12706239.545917897,2481628.3737554336,2],[12706237.196674753,2481630.3960426347,2]],
    25:[[12706237.112661054,2481630.39468592,2],[12706236.439912366,2481623.7366914977,2],[12706238.69215568,2481624.6282464326,2],[12706239.372024212,2481628.6819243757,2]],
    26:[[12706239.050420895,2481625.683578646,2],[12706242.41809561,2481623.133526292,2],[12706240.408882342,2481620.4966500476,2],[12706236.68902079,2481623.8962024427,2]],
    27:[[12706255.004955698,2481639.877449906,2],[12706248.922843812,2481632.6267743283,2],[12706253.14532219,2481629.313084038,2],[12706259.186160395,2481636.5242225355,2]],
    28:[[12706245.664062709,2481627.1155061973,2],[12706256.990451379,2481617.710671933,2],[12706251.213356214,2481611.384155884,2],[12706240.153916564,2481620.7292474024,2]],
    29:[[12706259.649748644,2481623.0265355497,2],[12706255.828891588,2481618.4167990643,2],[12706256.891529988,2481617.773131731,2],[12706260.759526545,2481622.111524689,2]],
    210:[[12706253.236929674,2481613.2524313033,2],[12706249.817585494,2481609.292562529,2],[12706256.858900817,2481603.5104907188,2],[12706260.452737488,2481607.111157545,2]],
    211:[[12706260.288000325,2481606.953345549,2],[12706260.439772727,2481604.835387019,2],[12706258.79825341,2481602.9470575107,2],[12706257.460010769,2481604.2442394863,2]],

    31:[[12706307.97110693,2481665.1115858085,3],[12706309.09210214,2481664.0827193595,3],[12706302.632898113,2481657.115078412,3],[12706301.46637343,2481658.137633127,3]],
    32:[[12706269.925245425,2481621.8900802294,3],[12706310.112903664,2481584.884108209,3],[12706308.971403144,2481583.7629125677,3],[12706268.901424294,2481620.732849078,3]],
    33:[[12706256.10238778,2481626.9582356084,3],[12706263.899863847,2481619.711465016,3],[12706261.469842294,2481616.9897179063,3],[12706253.61589118,2481624.114388621,3]],
    34:[[12706266.413625097,2481625.123777682,3],[12706269.987089824,2481621.8950657635,3],[12706265.39157394,2481616.994924826,3],[12706261.573626902,2481620.129735858,3]],
    35:[[12706270.287926363,2481629.309103816,3],[12706272.692236207,2481627.0098044486,3],[12706268.437970359,2481622.4173021056,3],[12706265.833683446,2481624.622560045,3]],
    36:[[12706273.235573024,2481632.371456954,3],[12706283.556625323,2481622.9620307824,3],[12706281.426548786,2481620.610074188,3],[12706271.31103527,2481629.3401503144,3]],
    37:[[12706276.590770727,2481630.8452505656,3],[12706284.283824787,2481623.7342650145,3],[12706283.527026732,2481622.9438043097,3],[12706275.878032703,2481630.0246423837,3]],
    38:[[12706280.91506391,2481635.38026381,3],[12706283.298786996,2481633.283318253,3],[12706281.747132966,2481631.5788575266,3],[12706279.221837103,2481633.656203413,3]],
    39:[[12706279.412620246,2481633.8722357145,3],[12706280.151479043,2481633.2594281263,3],[12706277.110684546,2481629.988612513,3],[12706276.43255511,2481630.6695450316,3]],
    310:[[12706284.753411854,2481639.647705497,3],[12706285.856941724,2481638.8412707644,3],[12706281.44615355,2481634.1576819587,3],[12706280.328613684,2481635.0507196616,3]],
    311:[[12706301.826393764,2481657.91321085,3],[12706302.712401321,2481657.095982598,3],[12706285.600852277,2481638.7859520772,3],[12706284.751443272,2481639.503258897,3]],
    312:[[12706302.805209907,2481658.3101138007,3],[12706285.322985549,2481657.5916959564,3],[12706285.17864242,2481655.312627209,3],[12706300.75872388,2481656.045766625,3]],
    313:[[12706285.22508292,2481656.6027866704,3],[12706287.192514105,2481656.528952154,3],[12706287.229530374,2481641.0316628856,3],[12706285.972667955,2481640.150733758,3]],
    314:[[12706284.480754849,2481607.4280005554,3],[12706302.068973033,2481607.7993304785,3],[12706302.179477524,2481606.3352071964,3],[12706285.32316888,2481605.938795012,3]],
    315:[[12706299.655121068,2481607.3986627935,3],[12706302.249950323,2481607.50300619,3],[12706302.442208964,2481591.4820534517,3],[12706300.319737101,2481591.944483468,3]],
    316:[[12706269.54889022,2481631.8808014626,3],[12706272.332546344,2481629.474115734,3],[12706273.701717427,2481630.7451586165,3],[12706270.87048503,2481633.2003302043,3]],
    }