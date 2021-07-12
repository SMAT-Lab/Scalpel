my_data = """86	440	233	83	393	420	228	491	159	13	110	135	97	238	92	396
3646	3952	3430	145	1574	2722	3565	125	3303	843	152	1095	3805	134	3873	3024
2150	257	237	2155	1115	150	502	255	1531	894	2309	1982	2418	206	307	2370
1224	343	1039	126	1221	937	136	1185	1194	1312	1217	929	124	1394	1337	168
1695	2288	224	2667	2483	3528	809	263	2364	514	3457	3180	2916	239	212	3017
827	3521	127	92	2328	3315	1179	3240	695	3144	3139	533	132	82	108	854
1522	2136	1252	1049	207	2821	2484	413	2166	1779	162	2154	158	2811	164	2632
95	579	1586	1700	79	1745	1105	89	1896	798	1511	1308	1674	701	60	2066
1210	325	98	56	1486	1668	64	1601	1934	1384	69	1725	992	619	84	167
4620	2358	2195	4312	168	1606	4050	102	2502	138	135	4175	1477	2277	2226	1286
5912	6261	3393	431	6285	3636	4836	180	6158	6270	209	3662	5545	204	6131	230
170	2056	2123	2220	2275	139	461	810	1429	124	1470	2085	141	1533	1831	518
193	281	2976	3009	626	152	1750	1185	3332	715	1861	186	1768	3396	201	3225
492	1179	154	1497	819	2809	2200	2324	157	2688	1518	168	2767	2369	2583	173
286	2076	243	939	399	451	231	2187	2295	453	1206	2468	2183	230	714	681
3111	2857	2312	3230	149	3082	408	1148	2428	134	147	620	128	157	492	2879"""
my_lines = [list(map(int, x.split())) for x in my_data.split('\n')]
out = 0
for line in my_lines:
    out += (max(line)-min(line))
print(out)
out = 0
for line in my_lines:
    lin = sorted(line, reverse=True)
    for x in range(len(lin)-2):
        for y in range(1, len(lin[x:])):
           if lin[x] % lin[x+y] == 0:
            out += lin[x]/lin[x+y]
            break
print(int(out))
my_num = 368078
for ring, x in enumerate(range(1, 5000, 2)):
    if x**2 >= my_num:
        omtrek = 4*(x-1)
        omtrek_waardes = list(range(x**2-omtrek+1, x**2+1))
        break
index = omtrek_waardes.index(my_num)
index = index+1
print(x, index, ring)
while index > x:
    index -= x-1
if index==0:
    print(ring)
else:
    print(index, int(x/2), abs(index-int(x/2)))
    print(ring+abs(index-int(x/2)))
l = 101
target = int(input())
out=[]
for x in range(l):
    tmp = [None]*l
    out.append(tmp)
x = 50
y= 50
out[x][y] = 1
x += 1
current = 0
dir = 'up'
while current < target:
    current=0
#     print('working with {}'.format((x,y)))
    for x_mod, y_mod in [(-1, 0), (-1, -1), (0,-1), (1,-1), (1, 0), (1, 1), (0, 1), (-1, 1)]:
#         print(out[x+x_mod][y+y_mod])
        if out[x+x_mod][y+y_mod]:
#             print('checking: {}, value {}'.format((x+x_mod, y+y_mod), out[x+x_mod][y+y_mod]))
            current += out[x+x_mod][y+y_mod]
    out[x][y] = current
    mes = ''
    if dir=='up':
        y -= 1
        if not out[x-1][y]:
            dir = 'left'
    elif dir == 'left':
        x -= 1
        if not out[x][y+1]:
            dir = 'down'
    elif dir == 'down':
        y += 1
        if not out[x+1][y]:
            dir = 'right'
    elif dir == 'right':
        x += 1
        if not out[x][y-1]:
            dir = 'up'
print(current)
my_list = """nyot babgr babgr kqtu kqtu kzshonp ylyk psqk
iix ewj rojvbkk phrij iix zuajnk tadv givslju ewj bda
isjur jppvano vctnpjp ngwzdq pxqfrk mnxxes zqwgnd giqh
ojufqke gpd olzirc jfao cjfh rcivvw pqqpudp
ilgomox extiffg ylbd nqxhk lsi isl nrho yom
feauv scstmie qgbod enpltx jrhlxet qps lejrtxh
wlrxtdo tlwdxor ezg ztp uze xtmw neuga aojrixu zpt
wchrl pzibt nvcae wceb
rdwytj kxuyet bqnzlv nyntjan dyrpsn zhi kbxlj ivo
dab mwiz bapjpz jbzppa
hbcudl tsfvtc zlqgpuk xoxbuh whmo atsxt pzkivuo wsa gjoevr hbcudl
gxhqamx dradmqo gxhqamx gxhqamx
yvwykx uhto ten wkvxyy wdbw
kzc ndzatgb rlxrk hfgorm qwgdky ndzatgb rhvyene qaa wxibe qwmku nmxkjqo
qwx ubca dxudny oxagv wqrv lhzsl qmsgv dxs awbquc akelgma
rrdlfpk ohoszz qiznasf awchv qnvse
ggsyj czcrdn oolj sibjzp ibzjps asp
vbcs ypgzae xcvpsr ptvb leoxqlq zmpt fhawu yfi tvbp
ejkr qlmag nsz jwpurli nhsml asksnug mes
kkgkjml kklmgjk kjgpx iquytbj eccceb mfv iuyqjbt ovv
uoklkco zzey sdfhiyv ytdeg
azr mjv raz arz rdfb
pir dafgsah dafgsah kndjbml estcz yjeoijp kkcws ebq puwno
iqymwc tac vlqc bmnkz xustm leqi
gwdjed cfha axz xjuq
abfjsg pahat qlj zan qsfn iozfys jnvu bis jakggq
afwuejn zrbu zurb hrn lwvjb jnwixla aufejnw
vkqn cuzf humhriz webnf uzfc zfuc
eznxd kgbfy jqyc net vzfege tprzyc
mqnapzn vrgw ilzp vgw
aie zkkih fhpwu bbn fhpwu wvxxgmd
ksoasrn yll mvdjxdo wydymx dmodvjx drnjlm tcjpjhj xzakb wrsbuwl vaygdwf rsasonk
qahbh tfhkl apdqqpm tfhkl nsox
xkelwve mvdmesj xrto tgku gkb bpe
nni nyylpu cyusxe zydeyok yokzdye xiscesy
itwsfr eqwrx igqkvif whklwdb
lpa hwci suwqfln xis sfht lzek ajecd
svpf eulute eya gvmsd app claria tjtk zjt agdyemi bixewo
gmzglxi zlgouy bejg kte xlf giquj mjeq ivjkw ktbhaga hoffyrt
wwjy dtf ftd agei yde xhbfo fyridy
gexcy hetkz ufflrfi frifluf plb kqre etxo elg henqy fspm
khaemn buec ichau wxctsxg
cgmv ujyvcuu jta yux ccx skrafkn cmyc yidqhv ltb ycnajry zitq
ybsahqn pio veeze vdztjz iedou pio sue ijbz gvqncl vpa ijbz
hkfi xzrsyke hikf mxolx xlxmo ungfc tst xjzd
tpx ioprco qixlv ipocro
oahmwrv homvraw vws ntmbdvx
fxlg wnuz ogt bxgtul vmfh nwuz glfx tgxdq bxfv kajuh
vrhqn nrqvh tgogb vya ragbro ulrz uava kexoi yav vkfe
bxxy tyxgxd oabsud bauosd jlch bdmrqq wqhjwb ayblb hclj
sfzsgsc sfzsgsc jbrvh sfzsgsc bdhy
wixleal vhnqbfw qwfnhbv woco oowc
exkkwz wekxzk krxbua nshxqgh
gkn blxgui nkg gnk
otsa isqn otsa isqn
ude xedl ude xedl amkktp
teroe yuvbd inf mpytuvz xiq xqi ovqetn
zyq ybeifwx fvoqp vhoduy bcq wbxl
zymiid vafcqv vjbmekf lgxkma bjti qfavcv iqp fnbu lakmgx
rkaqvd vylkh jfdxh imxxg bbrt imxxg rkaqvd
yajg qnhhs bzmb eyk hijcg tkij iwr jvwp dipzd jvwp
btzhw zttheyo ravsbz bmbba majoe ykrs tbxqf tai cgsvpu srbavz
vsyczfs ymg vsyczfs wxlwaqb oouio owek wxlwaqb azvbqiq
ghrapd ghrapd wisq wisq
znmleu aztnkbs wxc gycxd vqenhh geqyo rpjg
kxbom gzz zzg zgz
dfsesc okwb dfsesc okwb
egpwqbe djlk xpkxa hoo eepbqwg
nxdfror yfhkhn zgea fkspva rjgg bnmq ddsf rjgg gkinm
vdrxfom wbdwu dhkt xtvzc zjobo aqvgrt
svddsgz mhcrbcp wmpd mhcrbcp klim ddlnxv wrdftrc ddow wrdftrc
obxr wscs new brxo wen epns cvjvxts ilnc
rwezl vmbut kgblt xfg vnhlebq nzqdzxm ynh wokrezy zub nzzqxdm
vephajp bzupele mltzglh sbgn vephajp lhve mltzglh
slajp kyaf vlnvy srfietn ayfk inaufex fanuexi
vazwg kjg qanzso ptuu vvlwq uupt kohhql jkg
xmmmpky rbqimi slvxsf tlcwm pbf pks iucx rbmiqi
irkup jvu tkeioz avdu suxamf
tmgih ldca jswka dblzzt rap rgqyy gyrqsk nnnn pok
pdbjhrl gsvxbqr nqfkhtc ngn okbgzd pdbjhrl oostjtm okbgzd
mzqfdat dujh aeplzqh acbguic vlzdt amyszu amyszu jqecky bhl hjqnimq xoy
dszafr bqampg epozj sfrlpe dszafr wfurku sotjpg wagtnxy
jbmo jbmo plbfkvw bkc jbmo
ehelldu vrid unnf vrid xqiu tbibjyi bmbpsmq tpqyefx xqiu
rpgm zzbj cjgfdyb bdjfgcy rzqecd miyvfbu aqlkagf hsuxwgl
gvywzp phvnd ypwypbm yfelxx egbr lcfyz hecdhkj xxfley
tsmebin tbsnmie mkijj ijjmk
cghxrqs vzxle wrfghv skighgt zviteab plcrgv
ezdirp rxkw horcek qcgny inx nikb tigzp
eidk sactjci sre vkapava owvf eyds eyds
vvjdm uye tjixj azklizl pnb
tcrimv xye twii xye twii tad
mtxcg lwjxdj zjudqu ekoujd ysf ajtfta dkj lwjxdj
aowhmvv kkic kjize fnohl ukx remfmii usbp
wkossu limxmhp xnoeocb wkossu lnrlqf kjozfg xeulstx sjncsw ekaimuv xnoeocb sxjegcg
lsfe zpewzlc yhjyiay lou ukhi lpwezzc slef zvtidgg kdeseq enka tfvgudr
ovfsa vuv tbtorv tbtorv gmxn opspw lli mfzvkv zlyhr oznalr
kugrpw sduq rdc ciaxwir ylnzwec kugrpw sduq
obevuau thu jpyfvof rpawwo obevuau gsvoutr quiaei
xpgua pbxa pxgau kdan
ohyzqk abxgg xozgai nib axozig bni fucgykm jpkswt
jrgu dmozts jrug ufpho
qojzue uzeojq txuhj eqjzou
wcvj qwlravl niyxf oiaptlk wlxnnzj jgdzap jgdzap lfgn bdt sfga adrypo
ylah eedu rvwdpmq eedu ylah
quages kmla yjqua dzxcfam srjag wujmcv qujya ssaol uzdwi
gdsppz yqxlish yfkjbbf ecnzu ejvtv cdjwre
slsls pcmrq zax btrc kliv ntho gymkk kkq pcrmq mvnw sjfegpx
ryz jfw eki wvibww qdzylg whbagp ffrfjg wdhnqpm hcrz
tcjqfh tmvzp mpztv vpmzt
xood xutgof teqov fqyyub oakm rzaheiq
axagoq jawbz sexucp sexucp atenr edekcwn edekcwn agl ecj gbje gipivfq
poqv qopv bos flhghs gshlfh
rxd dzphnb bwmna vxd rxd sbk kuor
kqeelq jqbyh xczqzqe jbkmx kelqeq xqcfqn
jdfy qzjyz xvqyo jdfy xvqyo
vyoqyd pwayqag eygmdt smakwc veftikz fzeikvt
aozgkne mpd mktgoew eepp zlwycr eepp hswbxcx nmi ddnfr eepp
dgpfp cfhhqdx vjrb uyimbm byx hfdhxqc
fxq jcouwfy uhuao zsab xjao
noudveu egxyuqw hmnnv vovt wmqkx syatiac whkd
gxyzk opgb kjxp delavq hsnvk kfn irkcfq lvc aadcwy opgb
exuiupk ddiiyvm nsggpj ddiiyvm nsggpj
hhjby rfejzp akxzs nconlt rynivtq voloj qwhhll ubvx yxuacz miuwxh ppe
uspqvx supvxq cekv niddfuw
optzcag sra ajs ozacptg yxkludq jjpvldz mxo mox
dko qyec iuxbrbj dlz jxribub
ywlyz vipfh amsfr fwiozi tahjov tap rsea zwlyy oqdyfbo
xeqml jwy eguc bvzvh
crp mxsihvo wwtg gsypx mxsihvo qpfw looca gewvy zjqki tdkuxo crp
mqlnzm yihsvrl hhtwcv kigymqu yswki hksk vbiujq xeqz irzcq cpnz
zxhfsw uuyhwid nzabem mmfk wszfhx shxzwf hqnrvsq
hfjajdl qwmk hjdalfj mwkq gqbku dsszk
fbiy pujq htgaqqq yro ztpe yiufb fnpi ggchdgz
sixq jsboan eoie msdrwzw sixq njsrc sixq yimqoi
pbxgv kqmi hjuk bbtrlta bqwm bgehofj ainqhm qoypsil manhiq ogebhfj lvmuo
wnax aen fthpcke tcz yadjmva mydavaj rcfkc krfcc
lkatiw zxliii usdj oopxl yylv bkjfy gtlyjv usdj muqazdb
yqonaxv wqnvoo hfpll oyxnlfs fgajc khhtzr hfpll gsvvipz wbjxsnp dcdikt hqw
vvuv kspmnz zvmryqd egvuz eazkhz kspmnz
xgq dziwiym gsl nbzmsta ccbzn yalof dbbugq aar ywmbvk yofla dcwb
qrtyhhw xeyo vlym ulzzbl hrxyb qeyu jqdkewk oxye evaxz kybc bssyt
eqrf cfyy kwhohw ozg jsc egz jsc
vct cet ixxvmz ibhvndq eks dpi jzfwdqv saeh jqzdfwv vwfdqjz
vus vus kitvvgq wpi alfncf gzj oxcy fith oxcy ecbsr
uacculk guwhwdp cankcv yswy bmby sve dvonm nran
ydftm wszgaex rgbw otd dbet lhsxndd jqfyx
vhawg hwagv uagy fveik nrsew zujw hawvg dzfmt agzgw
uqdj talb uqdj aizyuqm
pbbejee szdtohv tycfow xwne qzlqy dxcwejz pqdqrc wfyotc gdqt uxaeug wtldm
hmzmd oyp pyo opy
qwdh kwpll kwpll zsbez uxg klr uxg
myqr zza kqpcos adsql eumunrv qlaeumx
acyye xvdewe nwkhuz bzcmx asw ostiwk mfzu nwkhuz
memq uqadd kfj dses lrxb hxygp dsse bxbr hgpxy uavrar
mjmk lsdttuz qjkg yfthmkn pram
pctfq aly usim shihap uims xkfgp ksrbn ifvsyl
cdma nnnu hdm dhm
kpt upgsm ohvrrqf qwps wjcbve ohvrrqf
wowphgb nteme otizypb eumgvb puoctli opicult wbohwpg
fppz ftkql sbut lkqtf svif viqhlnn buts lljhbd
oqk uinby rqy vbjhf oul hzfo coca glpy brjy yglp qnvhvei
sbbwr dnyrux gpikv nsx aawyeq uhtucwq rhxzy jgx bdgdrl dnyrux lgfgi
agn mljz hgmglem popu jtapub agn
ehfpgr bnobvg bnobvg bnobvg
ozgzedn godezzn art atr
urz rzu xzyc rjhwi kgiodi doiigk layr dwbxu
rkcbav pnp bpsmm ifivfe csouqpw fyswzbd csouqpw bnjt rnnoxed
hpjgtcc ctcpgjh cchjtgp lxn
cinokbx uyaz uyaz uyaz
bphfwad bphfwad bphfwad yml izlhlb dvjvo jeropar
ocgftcl wshjk zbinw fcotlgc xdj nwibz
zbze hllno rmq invd gupoxr gwumc vnzj fcvvhjo dnn sfsxw
oqlhkz hgf yxiahks vhzvl ayshkxi irmwkmq
apeqic ahwu abxjrd tuwrd pynnil eohmlgo lafx ybpofe wbznxv swuafas
cpg jpsfo jposf rer ixeydpz
rhqrwvn wrhqnrv xptms jhc rnqvhwr
zfpl tukxzda lifkqtd ynfuno cttx ctxt tlqdkfi ueswv wbipfbe
eblw bwbjg fuu qqm qtv qtv isbl denfcb
ick yqwcffk pvcchd apkjyc ouu uyfe nplid ick caqscs sddkx
rtzh idn snnw xmlou idn kdhenl rtzh ujwttl pkynkhe
dnwha fpv dnwha iqi xggepo dnwha
yjvk saay enxqhw wigoah dzasyr nnt artl iqwia jpp xmfr hwigao
ryt heenuai ytr gqew hyb byh wdurx kmd adgjz
ypdqeji sfkkfhn stms cdmyh nqllx utiphia gxbx zflhtgo yurztx eni
pwlhlt lhlwpt rfkvlgr tucajej ckujc ntcyae xestygt eshmggk
gtfb codwc vjtli ffmjwx ruoekt cylrm ktroue dfaxzvs kkgejzi ewucgu jyatrum
ersbag cod xssha aqzbe kxu bzghhqk pbs bizvqk bhbbd bps
vhci ypxf bxzor unngl xilpzpk civh nykora vchi
cyb cceu negnld nbcfs pxsjgh xah nbcfs nbcfs jabpxg wtanv qhztvr
cljgzkn lrdeina hrjoz kdgpn vqkmpal nivk scvnu vzuausp
nif fin uxjbip xxztsn yyo opueh zxs qnso paedey hsd fttvqdn
gbnkmpr afo aof ryyudy gbmpnrk
uaa npb dkit npb buadan esv npb hwrj
hws dfgq fcyty qszhu chyxxl ytmpb azxl jrsn boqrx
hkzlnkd fkilvog xbubu fbgbp
fgi inmay uliytc vgkcw qsoe uliytc isjhix oyir ocaq
qrzkpm dpzetbr zommsxo cixg nwjyvp bet wyjpvn cgxi tsncd
uvlf lufv ulfv cigl
uwwf thr kdq fhjmty bvxue vcwwmk kdq nzajq bxkf
qcwduju idxaja qcwduju idxaja
fnarz pstzfne nco qzf kcevoo qwx csvsxga pstzfne
twug xrwy uoctfl bkh yxrw
unpdnbe apf cvm bpullu fyels tjpri jyw unpdnbe xfyekay vhk zpyb
rbv psirdv psirdv mnjrp qpwc vicismd qpwc
zjj zjj kesyhow eqcfqy vqy
zazpd gmea aobl dcs mage hqjdpwc bvxr srw
rhcdb nzsa jgcgc rhcdb wxs vsvvptn zvckqo wxs
unyet prchn fiwter wvgknes dvzbxfs ufet neuyt fczlrx bpocdci vdsfzbx
znfev fwrdarx knqkv ojiv ojiv fwrdarx
tbtlo hdashg kyspxm ypmkxs nmrk
fzr zqxaszt frz xzrre
shueb iraetk uhsv duvah uhsv zstysc nrfllbc emrknka
vzkrmp mgtkjnw njr bwjgp jdwyyhv yudha wbvmx ewu urhiioq
yjq xxr swvm aipdj apjid tfsq gfqg izrvhev
iljuqt fpo fxadit iljuqt iljuqt
zrj poewso vsje bsprbmc vsje yfwf ybu dmkqib ybu hlrpdi ymh
apxaeq bgdm mqty whyay mnuzfgk awm bgdm mwwi ekw bgdm
dpdbfkm crrg mkph kphm grcr ukbk
ilqm wroz mqil qlim
pnlx nwadw uabelu rueamxr wjer uwge jwer ywagrx
akuil nkh oitq werli werli
fkmhcr ieoj xfsa xfacoeb tcg poomcme vck zmpc djcqgkf kft
csyk qni hqfrye zyyxz ggynzad pjpokmu bigqa qie
lkpenw zyllii qtbvdq zqnu ichftg xazped agl irhlbiy snlwfe twliar
acsrba dzz ivylbl rfcdd rfcdd qcg
zbui fomvpx zjhmgl sivtffu xuhswzt fzeid tgj mzok mozk afbhuje tzswxuh
nupjiat fdxkbn tuatp jhdfnub yitdk yghqw nupjiat ibi edfv tuixw auwjm
focht mnprh tljj ayp
pjdnl uaoworh iqm gic dqlu spn heuymio
kvg ferrvhp unvzsd qdcpd rji zpch
nhvay chuzg pyhdd hnmrnq zeidhf pyhdd ohy hnmrnq
boa sau gxh grx
gwo utwpd zcsrx gow bnm
xoqniyd hmithl xoqniyd hmithl
yqqsbzo stca zcsjnqf skbueeu tlbkef mvqbg igzr wujuz yqqsbzo kkfe
wgzuepu wge fkrxuag csenx tkngoz wge azueyxs
get xiryxs xiryxs xiryxs
wammvx edy hahetl xmvawm dye
lscxxgi anmax quo cqprwn imocarq gnbfhe rcnqpw
znpmid yaluvzn ydm ckh uhso rrk wbby lwxsu
atppk byf dzz uift nqejgm njgeqm
dtqmy iog ahub habu
hkthdwt pfxlwsu hkthdwt hkthdwt
tsuiue tsuiue yais tsuiue
swooqmp rqrcs ngr vujrq inuu rqrcs
dhu zxdfiyv xuz xuz mgaty mgaty
kiiiz zco qdv vfgkj rders zco
trszp havbm redpeqk gktp ifvzvwl yfoxnm tzg avzd otiouso eks lqlutwb
cfiru lpdy kpeas mdc lxnjjqz nqyyb xkjsug rcifu dln
jga ijgkjo qhbnupb ofzqn iokjjg gaj lrh pkynrcr jgatk
bexwc tat tat otsngaa
feh mjxbs ehf cyfhlv vvdgdu hef
njlvq ojwaes awsejo ktyvxd qeyeze bpoaj ulgngn zyeqee kqc bsdzzvq
hbfp vnhs vnhs pko pxnxgm
bmy bzpn bzpn bcfep
cju nqjy yjqn bbrj esgzw swgl bjrb
cxvrshm rbglkyv kqwzcyd azqr ckwbbew fhgqv nfk lactzh ssqpwbr wbewbck
ptcb gqkb apcc okl jbbgk qni bqu slydyo qhh dqd osv
zbisefn bmxcljk bmxcljk arkamus vpq uxuwvb
ksik xbzk lahh ctfur sxh rduokr xqou zwbgqsp skik
hwhmfk hwhmfk bjpxzg qqftmu ijyv igvayf bjpxzg
askxqew tibx pqaczy fhzyec echzfy cezfhy
omzyy mbzfvsn kkoff qgqn crnnkn krx oqp jhn anb qte qxt
jypnwn vjbnbsl axf pldxbq pdoy rmxcvig cpad yhah rzqewkg nmzkkr erjo
visidzp bujlfn xuomjj mjnqn wgflg skb
oer oer lfi zyqnem lfi guljz
fannhwu wafma gcje cvcia qwyh ugtbpa geufqg
kwtjib pqwai tdmjj kuxr euzl rxuk
ovi splc hflutgw hflutgw
gvel gelv aeiygth elvg twwr kivxrrj jkmqa
bas ylxbdgn yliv pytkhq haujsyf fggrnbc wsgree rfnppcx key gvdzgfy evdtrrz
oblab wpgm bpyy xuroy qhb adqko
hneb law uzms fhhk yjymdx wjla ixfh yblh
qlvsd bxsq hjaq fuwspzu hyshq idbabc rqcih ilixp wft rglf lmqm
qdskj two ckd qdt hzjvd woo fmmuw
kumc zywzq srafcbb ihfu kfvav
qlkkrq qlkkrq qlkkrq qsc
hob bpecik zqtrfz iqizeu plrer epm zqtrfz xrekeql xrekeql
warszd sxyyorh sxyyorh eztjf warszd kszp
hjbrax liumjue liumjue liumjue
rfnqd folmiu dlicln pdyk uqd rfnqd
mjdu lytfvya xomdujn leaqiyc lgemz lihfnhv zgeml koukz luqda
yqsz zedjmwn aep qwbhd yqsz
etg rmovps abizj yqr kib
yznxec sfqkd ofkzep njr hmeym nsh xdq
ryoyq heoo zuo udvfev ehoo axcnbpu oeho mfenmd shrebzy
uaeh jwllsjp frkhqsy uaeh
giofw hwceb euikqp ldmb kqpkxwv namazcg hqyyzgs cglsqux
qledbd qledbd kbwo wgfmgp
olbsca muxw nxs locsba
gbxxgj xlzm gws pkpwy ofkxb sykhdo nbhrv
najr bfk tbqkm hxabe nvr mdi dmuujr bfil nyripr zcydzy
kiczhcn dfgylw yzkwk nytijj pceu yukj ekaol xpb uep
acyyxn rwczsud acyyxn payiek inusyb rwczsud
mzssokx bshs bshs ocrvlug nzsgvch riejkrd jkj mpmdgsp kvixdfq msmmx
uaxy wpvhf uaaq ranp vfhwp iik kii nvh
shecxef nqpx jly dzm qvmpu kxg hdg
xembm yzevult ljrllc yrlskyk zas wstnz yrlskyk vasra
yoaxppi kzax hvxfezf mek teo cbtlrfa ncxac yee
dzfpbi cynov dje vxypba wcwww cwnu cqtp cnuw wwwcw rkzas
xzwdt jcwv anb xzwdt
fodgjem fmmrsfl eovsneo etzutda paw fmmrsfl jcqql
yfztt alcw nwdmd afgknu njxkj zykz cvv jbnl han iatmruu trqls
yas hpulrmf dzts sltg qsbw fjj rjymnnx dkkv
hwjtgd abmb cfw xoumxn xnoumx cxo xnxmuo alb
hnl zgdiip lrddhl fyw mporhtp waedf dltdfmc lyipoth ubmg hnl
wxard wxard cibp nzquvb muuslvw igvewfh mika wxard
cjqjhva rrhzy qpdc nqnyd enbdee ewrhp cqdp xekgjai
axtmxb axtmxb phl urdqaar urdqaar
umce jult bkart dgdvdwc kqzlzn nqkzlz umlxx cmue xvehqag wxifal
lwsuc ski ubo ksi sik qwcudv
husdv tssr gfp bfzbrp jtmk svvdpb uvshd zbnpdmj svpdvb
nnbvf xbb dobqk xwloqca uxvqti blcwxpu kubwu nognin goywn
xhe dhddftc ggltd dhddftc wspf
jodq cgvnk lpl wkwwlqd prfby bpyfr tbgyqm
bdebxj cuvow jdwdxw kuzh dvxmsyb dyvcxo psf kjnoe odfwgfa
xpfb knzgfsi thmsnbi ymjxn bevohy xpfb
hphcu fjodpdt mfsp jkvvp jvypar nlud lfv uftupcr nul dunl
olz ihyhw qntr lwcbohv qntr wzralwl
kfz pkjhidy msnmwz exox xexo uakipj mmznws zbbji ozispqb
gfi kwdhx qqo kdxwh fig
ehh rfozwr caoisw qntlk pkv zulc kpv hrqz
exmlrj aacc rzb qie rzb
mxyqe cuqz feyd meqyx gdvpu rqyjtvw dmoo vugdp emem
advj xmnad uvh ufnbi xmnad xmnad zzwjksx chbrjas hrbp ruvyg
nasrghk pmol ryko ofgakhd korf vpy nakrsgh
mylyqg aeizp rnk krlwchk aaqg
edxursp sosyv zesgnpx zlo sly alurdc ypmez qib aqtt lmxd
ihm hwzhd jhiw raocjk nlxce yzuzu nhudri tvygl tmclg mdkz
psubdis qrmxebg kdac xvl raxwfx vlx sxme
tci tphdy tggam vqqiyjz sgfvdri sxhztz fhsmxx yaj ncxcxq tic
xkljs cuhrm fdjqwd fuzyzh dzuzgjd lzpye lzpey
jriwl ypkcxd fxrg eit okzzzsc yaykarm qzuv jurgek dzfbbfl
workf rrw absfl gxluw qprdsz absfl qwqbmi amepvz oiqmy workf
dxyyb brnerbx lykd oqmz ursl zqom
cqtuzva aih uhaswd auhwds ktyvc hufogcg
jre fhlgrse svedc prfspaj ghm qcjzfc nsd
fow xyo vlvg sgg jgzvff rjxh eovre xtupnz
pekj pgiecc igxd zbiqoob ovv
xofxmz rdzdiq yruoqkh arfunx yruoqkh ucm bxov
ctogwj lpv ivtoxkf faj ctogwj xfzluad ctogwj vvw
rmc vjxj strgo tykifpp
ulivozu bczond ywnmt shakc yknr psr
bfx alwedh jfomlf pzj tely alwedh vccsoer rgwftcl vccsoer
frkwbv uudwt qsfg onuhiml jrd usu
bgdx deybefo gdj dgbx luu cbuwawd wqqtq dqmwy gin mhtfgy
ohjp ykemg nrs leayrh brtipx jhop phoj
utaep ywsy utaep ywsy
qow dxagjwb qbki bqik
larkpq bdgw mly vvwgv
juar zaerof qekpe hhgd eygru epekq dhgh
xpblz xksc lzue xksc yid nnve trlndn gjczngs cifqoaf
fpv ekz eknldf uqjgeu awwnwxu eknldf eknldf txhxv
mzvk wqtbda ovdbh vnes uiuuc uicuu bpwwtm aaat cygej nio gnl
rkdkzp bjaxqif xuwx bjaxqif hgtz slkqw rkdkzp ztp xfvgk ycvg
zpwr wvxzfcd opgcrfc ytxeboe rcqa ehrga lmgm
brsdnk nqgkjab nbjkaqg gho zqe
szbysu oqrtbp wjpuv oqrtbp oqrtbp gjmqq
uoyi ctscw uoyi ggn ija
fop lxa cgwpw lyvrxbe tit fop fop kfigqnu
ldqmk rxo ajhrbc ahrcjb xqdk kdxq
ith vdrl kvaxktm grkzmon ith ywbz kmnoiz
zdoo omjo fbz dveiipw fbz
ivj mcnu tkijlq xkq lrkyit cumn sfkrk numc ezxeeoi
lcwzdi sbsdgdy olvc olvc bimubzf bimubzf
cdjd umhwh djdc cddj oxheq veazlm
gxszn zsgxn azy yaz
byvmj mjybv jvxkuy akas uxyjvk
whmkttq whgzm gwmzh pkvtljw zgmhw jasudeq
yyjri fxsj xffmna vbal ftff rwq uszym bznil rfuctp ejndv wqr
gnwzjbw dezfvq gzkhzkl ivrdvxx wfah xvivrxd qzdvfe
xnfo zqzn iaod zlcclsd onxf lpskrfk nzqz kqzr kffpwak eky
muc tafbzp nra gvzc xiu gvzc
gfnbnyj nyjbfgn eoosw yjzf
qwwls sqwwl mxph swwql
twor uzjftq twro orwt
qomjuob bqaim zvfqww cvqzm wwipc zsywb bsqkp aoj fus
nlyd gtbgox tajlzgs bgtgxo pqt
pjtmgz ulblj ussh gngagba hhtexq bjbj obe xctciay osriw obe shxri
agc ejjdtak jgq moj agc iua syhxih znavmrc iih qubj
zxwzwhm lipkqhz bbv birxsj gzg iefrjh mprsfs ofpltbl gbo srpmsf hirm
rbpgqoe kymrf uzsut gkbtd xctpg qul hirtfl
wfvg pnqhuv jayjm ftqt mbrotl aydmoc lfwlxk vpvcsi svbn bnsv
jxjxza ysl kls vmt fvgunx hketl oshgie
dfeyxv akx qagwayp qrs lnulrle rqs gbvd bvdg
aac ndptml oke edwrg aac xechxz
mpx yrb oervzb ydvkw avlt oervzb bxdqbo hzwls
dsynfk dsynfk epexzjd epexzjd zofb
vhe zxfolqk lkh fxt flzkxqo lztwkmo khl
izlthi wtokkuz ousbpxp pvr uuxueq lvbeff mfk syjq fwgnfmg yytqesm gdd
kjcg slt khz atzw twpspdx kgyk wgq hjat ntf xvhxol msvdjs
ymm arrggw mmmbvrs ist arrggw nbvvc cwyacp
kuzglex iemp iemp jsko iemp oqs dheqypr
tzztq dsxqbow qgaeo kqn dsxqbow qqzpv
ysr fctpiyn psgb gatavv zsfxoxq nynfoh qaimoj zotjk nxug syr
xvm qvr hdxyhpf cbo xmv lfv wltyjlx
hjq pohc xgqit tducggu zdqmnc xqgit tqxgi srfyzu vdikqx
msiqte ewvp bzrv cmuy gse qqayvb bzrv qehy
watdvu ametrc etlduhh vcc luehdth udavtw
jktj mkq jktj mkq
uekth ufjkmdi qzhge wzwcwk nvrodcc vrcdocn bhcvd
xumywk zwofh kuxmyw acgzsjj hfowz njnz bnklyi
hmm fexu fexu hmm
zeuoarc yoa ggff jazzd mjein yhj qwo qwo
rolkwf fcyat lwm wqqm juwkt wqqm udj tex xgps nyy pdbkkhb
gld ksl gld bnsuhqc gld rwmybj
tvyxk xgmk cri pef epf unsl yktxv
muiql ejq taetjkf ejq xzmo wmv qbtmrh hkfbch taetjkf sut
pqg icvv gpq tufd iixd duft
zekx ybbb gzml vrbwcl opfb fkrv tto cbipr
moh stkkf ynrtdf jlgb kstfk ksktf
nvysvf mdtdoq bqqvr bqqvr
dqyz mzoqtp gzhdgd symsq iwh bpwox
pkqi jgzsrah yfjxx kdp xjaf lbj gkpixnj tyvzzso qmjbo skg nlchzbk
culxfx jarwu eiwriu vwvg gvwv sgnasz
kyfsn dwc sbnoe xwpgjh nbmvec dwc qjdh mpw gefimue fvqjwt kkor
hcdcgxs fof flc hfpjy lii fihcao pxg xywei jwsq yxr
oxrcv pda oxrcv gdvojsz kmlga mixlmp hdcabsn qvoa fwt
poe joylchz humrjy cyxbqfm lyk ybrfmp qmtpqyk vtpr lyk vtpr
ffswqs yxbuj tfzkmc yxbuj giog ckubbfy rtigw rtigw rpitxd
kcvrn eejyftw ejytfew rnckv
lvk lkv cooumh vlk
loypv ukowl loypv nyoyfl vehnm uff
tst sei zovy itdwibj mcbtst wcf rzp xvbtax ffzp xieenuy aegkj
zkhi hvsbgza xbwtdns wypfngy lvabd pybhcd crczm buikdpo vqgon pynfwyg phbcdy
ihy irxrj entmc yxfhbta xsdv xsdv
ezrcv kfgm pjneez puccy gzpxdlf gkfm yucpc mli xezfug
umjppkq idkiri wmnbhi unl nteyw wmnbhi zyv idkiri shhcrau
dzj zveqwae ljnikvb baavr dhsohp zveqwae goq zveqwae
xhc xch bmttdr snd jakd
jmgnvda bdpzfw dfwpzb pimpv blqtbyo lzdzo bgrlfy anmjvdg
lwvu ksg gqbtibd ksg lwvu ohfzlt foajo apyrcwj uaro
vel qksrwp zei ipnvd hdua rkspqw bujf
iozkiu upa knmcug zidypn yswb zswkvx naqsu
tjktoe dqpt pbqi dqpt
lcl tui uoizm xrdpmwi fbsuuqq tgeac hpajm tegac nczlic
ntmm mskzb arem ntmm jayzfe wyurgsh eqwcqt edhska asxhjv jayzfe
jyq juifidx fokzxh cgo xofhzk nhro xyccuq ioa nwk nqaxpfw
cvag bpk cuo ocu buehhq tartafi ifs qwh cveurg
bwut xpfni qzg cmp cid jftawv twiszmo
zgxc sui kypkd vpam ymxicrw jcfbutd fgx jcfbutd
tkxn rjqzljh tkxn mdwcho
qbv zneocv zneocv zneocv
tywf soncr lyepx qzj xdsr pdqv swt
ulu rdk iomqu dgouoba icax
ddsc oxilqpd ddsc atbekg ouzmxf oxilqpd kwtzz yhmyd otvi
vtj llnfrpc vfighju urosrsz vurtse llnfrpc qeuo vfighju nnn smsnp tfom
updfjmz ngtgi zaitq rqqhcyn ladzx zaitq fbaphyz hipe
rii fpos atl tal qhubqdv lat
whxzwdj yznkngr eefbmub wnxitd tnwxid zja ziewilm xylwn ihhsha lrptuyf
fhmzaxv mdn udl gyv pqw qlrz flm rqtji
bgn clnm cnml qyh hhf qqnur sgvigvm
qjtbysc ycbqjts gbgvlz vgzlgb dgxks qbvp grji dcc
wmduuq qayymzo zvh ylbipw sin ybwpli ilypwb
qsvzktt qsvzktt dasmg knh gcgep qai
jxukj qlgr cjssj aavqv
xpxa glsdfxq ngxwon ytuue pizqu
fxl vegoed tct luwm ulwm eeovdg
ntmpe auasx vkwgi cryuiix dmiufo fcb ldl jauncf gyouym asjcryc
lgwdcs eoxm hcrpnuf pcfnhru vlye fpurcnh uquukv vjc
lfns riwpdh phwxvew hhu jfptvv ofxd hkotgfq
qvuwnq wnpvs xdivrfz yaenqr fipwgl
vhcexfd bishqsc gsbruxm yzccyot yjloa aptg vbr gsbruxm ihqhyz yzccyot
knfst zhihi swhhq zhihi
qfto abhjx abhjx bpnijn ogmqxn rclqag dmeb rdogx emfriui hyvp ogmqxn
ivaemm wlsc dvjv aivemm xvf shfonv
vowhosr vptlu ucrut rdynh ttqvhg rdynh abtja pnvdy puxfmf dyhd
uvrenol ycuhvy ygm fjsxiwo oftstid ygm
fix qrqeg dfgvlun fix iraxgtt lhgqdo eqkgshd jwmrm qrsbzba
mxdj icjqzqw fvew gtvlhm mxdj
cyjtkm crb pmg jwo iluc brc ttnd
dasmgp ool ool opc
ubi pmz mtkh ibu hlx ipcvjki sydw zpm eewfdeu oga
avex yjaoghv yjaoghv lwwx
kwkdst iuokd nmpw onayet zlavwnd wwvbr jtrkyku wfxx dumydgh gnd zgi
ahyjnc rjakp bhabq tsmfi ahyjnc tsmfi yitqgi uwnywil shnkbn
krr sbbfjtm yvunas hwppsjf ntuuzw ngyvdmt ynk nfq mfrb pyw hngr
eeecesf phoo ijmx sjp kgmtg sjp wyz
qwixmou oximqwu ixu lsmf
dyrzq lbstdjv ldvowml qjf fqj zpabc dwmvoll jnq
pdtlu hgcfvz mnwjyq ymi cvcp kmx mkx ooffp uiwg opoff uevqt
hflomt fhlmto gutdbyp xyi zpggxc wqe
jpsr wwex yjgdj fqah wrmmw nyrnw hcomcgv teajmu emw zrraid
tvgsca bzgzkga ypsxsk dqz exmu tvgsca dqz qnd
arzn hojpi bznw ejuupe bznw hojpi
rids dule qaefaon sspit mtzgdls cfujw xldhimi igdoy dule
nefsys plea obksngc zxqee avsi obksngc vnsxdrl gspadob avsi owmzpeh tcj
oweq fkr krf rfk ztwjdry shzcmew jhna
hdjizhg dfclic usds luz mcwyj luz qvomls mren otax
pmzzfj pmzzfj wfxyq mqv hyp lhf
dxeaw ckkey ccvawo keaf izlh oacvcw lgcpgeh kdiky
xkwe xekw kwex tzfyx
dmmyt mtdnqw pdw vdav ofrtsk
klz zlk snxnihg snhigxn zkynpd
ijzce xobf uojezxi xiuojez
ztepv zvpet nije aditjlg natkkk dtitg jprgia
fesuh wadrhc bayf kktfaf nxvhq smbdaop gqx ioez fkjufb abyf
hej sta pztkcd pesabzz szp iada iada cdae hej sqst luf
xlnuhn oljaf fljao ascxez fojal
dprclb fzn wgauz rxewtp cjrlgz zfn
fidwoa mvoqy afian ntzokap mkplgy jfukgjv cyfsz
hbvqnnt giinuzq uezugy qooxjc zsxr rnihg ipbels
qroi wtltjq suj tqit bxtc jidzhpe nizp wtltjq nadcdm wwyhjrg
qtr fkbl bpptu baen awjpwsg vvqbxz animt uqbk zvbxvq
nznq fdiul jbv umyrf yufrm hrl duilf
bkvlfuw onkqzeo iwrg rifqzhj mgroul rnor qqqc sbfi hny zosfp kopxb
nvifbx jbowbj fnyskt jbowbj xvun xvun
piyl haajm stwzpp xvjg amjah
gye efwwwiv kyv zmtcgmi ifwvwew
dflx gdtb jyoj jyoj dflx aqhycgi xffnn
inc mpys mzqmcwx vryz ibqrzc pmsy fat rojpxwy rcbqzi gjef"""
def check_pwd(pwd):
    pwd = pwd.split()
    s = set(pwd)
    return len(s)==len(pwd)
assert check_pwd('aa bb cc dd ee')
assert not check_pwd('aa bb cc dd aa')
assert check_pwd('aa bb cc dd aaa')
def check_list(lst):
    return sum(map(check_pwd, lst))
assert check_list(['aa bb cc dd ee','aa bb cc dd aa','aa bb cc dd aaa' ]) == 2
print(check_list(my_list.split('\n')))
def check_pwd(pwd):
    pwd = [''.join(sorted(x)) for x in pwd.split()]
    s = set(pwd)
    return len(s)==len(pwd)
assert check_pwd('abcde fghij')
assert not check_pwd('abcde xyz ecdab')
assert check_pwd('a ab abc abd abf abj')
assert check_pwd('iiii oiii ooii oooi oooo')
assert not check_pwd('oiii ioii iioi iiio')
assert check_list(['abcde fghij','abcde xyz ecdab','a ab abc abd abf abj','iiii oiii ooii oooi oooo','oiii ioii iioi iiio']) == 3
print(check_list(my_list.split('\n')))
data = [1, 0, 2, -1, 1, -4, -4, -5, -2, -1, -4, -8, -8, -1, -6, -9, -3, -14, -6, 2, -15, -9, -5, -9, -14, -4, -3, -23, -24, 2, -24, -22, -31, -23, -5, 1, -35, -11, 0, -30, -18, -25, -24, 2, -35, -33, -29, -2, -27, -44, -19, -19, -40, -52, -26, -20, -37, 1, -40, -36, -29, -37, -56, -59, -34, -31, -17, -24, -14, -57, -16, -68, -27, -60, -73, -16, -60, -6, -45, -38, -48, -33, -68, -12, -51, -49, -10, -28, -66, -88, -8, -83, -5, -2, -39, -39, -12, -87, -63, -55, -55, -26, -5, 1, -68, -100, -98, -71, -15, -96, -100, -107, -45, -46, -3, -13, -25, -110, -63, -84, 2, -107, -11, -50, -8, -55, -96, -76, -26, -103, -42, -43, -94, -31, -112, -64, -72, -95, -20, -51, -27, -129, -108, -75, -92, -18, -18, -68, -43, -71, -59, -70, -122, -64, -39, -146, -134, -120, -3, -137, -88, -93, -155, -66, -34, -85, -142, -55, -141, -5, -74, -110, -32, -148, -90, -108, -9, -75, -55, -64, -14, -5, -131, -31, -119, -115, -170, -110, -52, -187, -44, -169, -53, -154, -79, -48, -26, -175, -153, -198, -139, -119, -119, -93, -80, -101, -65, -112, -186, -1, -171, -71, -209, -76, -121, -104, -159, -91, -54, -6, -18, -196, -40, -155, -103, -98, -191, -66, -83, -206, -142, -118, -211, -216, -141, -197, -131, -77, -46, -110, -124, -56, -165, -183, -94, -87, -55, -110, -208, -37, -99, -63, -86, -197, -176, -235, -202, -131, -49, -22, -247, -253, -256, -114, -49, -126, -104, -105, -87, -230, -61, -83, -24, -196, -31, -267, -118, -139, -83, -45, -251, -84, -187, -104, -192, -224, -145, -219, -266, -62, -27, -255, -2, -117, -240, -199, -295, -177, -185, -245, -29, -47, -55, -64, -147, -154, -217, -211, -291, -254, -44, -103, -271, -37, -244, -313, -200, -34, -197, -72, -309, -124, -134, -9, -244, -254, -160, -5, -84, -28, -26, -162, -261, -102, -85, -305, -38, -54, -57, -320, -94, -13, -92, -34, -114, -194, -128, -220, -259, -298, -76, -31, -185, -212, -10, -7, -329, -80, -135, -278, -264, -322, -82, -3, -9, -334, -89, -217, -56, -99, -16, -103, -167, -148, -41, -311, -125, 0, -135, -252, -288, -293, -18, -19, -358, -186, -117, -65, -170, -34, -256, -376, -81, -106, -92, -389, -147, -203, -335, -320, -240, -373, -337, -239, -7, -214, -292, -55, -388, -143, -251, -111, -240, -259, -187, -278, -9, -312, -336, -382, -226, -203, -318, -277, -142, -65, -80, -237, -347, -92, -166, -322, -306, -289, -64, -53, -162, -16, -357, -395, -57, -409, -225, -10, -169, -232, -326, -219, -59, -173, -315, -420, -432, -100, -434, -426, -160, -450, -394, -145, -146, -42, -320, -296, -150, -159, -129, -62, -345, -99, -378, -234, -144, -323, -378, -202, -181, -334, -135, -446, -295, -290, -202, -366, -333, -322, -311, -439, -180, -319, -264, -467, -397, -411, -177, -235, -280, -220, -371, -379, -270, -157, -75, -5, -82, -137, -161, -17, -423, -216, -10, -189, -278, -467, -506, -118, -435, -468, -357, -169, -333, -32, -266, -85, -515, -76, -80, -442, -190, -199, -173, -264, -314, -46, -360, -384, -140, -213, -32, -345, -367, -179, -295, -1, -8, -520, -300, -229, -538, -488, -291, -234, -159, -384, -318, -257, -379, -263, -495, -77, -227, -108, -20, -515, -293, -475, -127, -247, -467, -10, -29, -539, -233, -461, -347, -512, -339, -298, -419, -252, -333, -515, -203, -104, -56, -456, -101, -101, -68, -235, -188, -522, -558, -151, -337, -572, -47, -411, -177, -172, -178, -527, -357, -192, -342, -516, -215, -453, -183, -144, -13, -417, 1, -537, -588, -512, -450, -343, -383, -167, -342, -235, -394, -227, -580, -226, -437, -314, -460, -279, -7, -157, -125, -520, -208, -69, -308, -9, -554, -628, -556, -329, -60, -3, -378, -188, -498, -600, -639, -52, -577, -332, -600, -119, -572, -261, -58, -542, -115, -328, -15, -411, -19, -56, -417, -332, -449, -629, -440, -523, -284, -304, -302, -71, -87, -197, -160, -461, -348, -339, -367, -87, -352, -232, -598, -441, -660, -332, -228, -676, -387, -240, -222, -62, -581, -102, -63, -589, -37, -427, -238, -687, -67, -315, -408, -685, -6, -664, -64, -515, 0, -606, -494, -465, -73, -79, -553, -86, -513, -699, -8, -485, -376, -659, -214, -632, -694, -370, -35, -639, -373, 0, -584, -538, -69, -293, -500, -537, -476, -578, -566, -123, -464, -321, -434, -238, -651, -61, -69, -207, -297, -537, -456, -122, -80, -517, -581, -411, -418, -734, -536, -278, -92, -416, -573, -308, -302, -645, -555, -314, -33, -715, -484, -89, -746, -254, -334, -509, -651, -556, -615, -447, -239, -545, -173, -4, -390, -526, -252, -654, -747, -313, -430, -625, -625, -578, -407, -28, -113, -54, -404, -671, -483, -801, -530, -191, -41, -694, -209, -158, -49, -608, -43, -34, -710, -96, -417, -297, -553, -310, -206, -634, -419, -795, -104, -91, -687, -105, -248, -693, -286, -63, -33, -199, -68, -248, -297, -281, -692, -654, -521, -240, -432, -515, -58, -711, -671, -433, -357, -228, -531, -457, -269, -76, -428, -590, -533, -787, -833, -453, -199, -113, -274, -144, -495, -481, -727, -356, -164, -711, -143, -503, -702, -783, -858, -494, -114, -18, -615, -243, -306, -312, -378, -823, -689, -119, -228, -769, -508, -298, -77, -465, -447, -348, -392, -751, -642, -841, -654, -617, -119, -490, -139, -359, -58, -34, -554, -168, -675, -104, -772, -232, -124, -460, -815, -856, -260, -3, -303, -771, -398, -282, -353, -192, -227, -645, -598, -345, -197, -881, -242, -159, -693, -537, -887, -44, -302, -252, -496, -590, -126, -883, -301, -697, -439, -928, -69, -192, -30, -273, -944, -606, -319, -638, -319, -391, -573, -268, -231, -649, -781, -936, -434, -435, -287, -282, -778, -608, -844, -708, -26, -162, -697, -168, -280, -472, -96, -470, -334, -38, -739, -936, -655, -946, -599, -562, -12, -912, -406, -532, -458, -828, -764, -314, -880, -897, -499, -412, -774, -249, -579, -294, -883, -558, -963, -228, -775, -205, -515, -662, -335, -926, -2, -865, -763, -23, -543, -715, -243, -343, -176, -68, -326, -926, -481, -517, -517, -885, -238, -400, -560, -390, -96, -285, -213, -680, -221, -856, -451, -33, -391, -589, -443, -695, -276, -415, -362, -789, -909, -905, -71, -919, -644, -237, -239, -458, -705]
def solve(instructions):
    start = 0
    steps = 0
    try:
        while True:
            next = start+instructions[start]
            instructions[start] += 1
            start = next
            steps += 1
    except:
        return steps
assert solve([0, 3, 0, 1, -3]) == 5
print(solve(data))
def solve(instructions):
    start = 0
    steps = 0
    try:
        while True:
            next = start+instructions[start]
            if instructions[start] > 2:
                instructions[start] -= 1
            else:
                instructions[start] += 1
            start = next
            steps += 1
    except:
        return steps
assert solve([0, 3, 0, 1, -3]) == 10
print(solve(data))
data = list(map(int, '0	5	10	0	11	14	13	4	11	8	8	7	1	4	12	11'.split()))
def solve(data):
    length = len(data)
    steps = 0
    seen = []
    while True:
        if data in seen:
            break
        seen.append(data.copy())
        index = data.index(max(data))
        v = data[index]
        data[index] = 0
        mut = v//length
        mod = v % length
        data = [x+mut for x in data]
        for x in range(mod):
            data[(index+1+x)%length] += 1
        steps += 1
        
    return steps
assert solve([0,2,7,0]) == 5
print(solve(data))
def loop(data):
    length = len(data)
    steps = 0
    seen = []
    while True:
        if data in seen:
            break
        seen.append(data.copy())
        index = data.index(max(data))
        v = data[index]
        data[index] = 0
        mut = v//length
        mod = v % length
        data = [x+mut for x in data]
        for x in range(mod):
            data[(index+1+x)%length] += 1
        steps += 1
        
    return steps-seen.index(data)
assert loop([0,2,7,0]) == 4
print(loop(data))
data = ['uglvj (99) -> ymfjt, gkpgf', 'vvwrg (51)', 'qrpgt (5)', 'qhqbqj (55)', 'taxdaf (23)', 'zbbdyc (81)', 'xhymdo (185) -> errip, lsppdni, mxukll', 'qlrcubm (81)', 'ukgzz (7)', 'ubvvr (288) -> hrpzu, msjeeks, ozizlok', 'zfotzg (45) -> ovomgd, mqhwlq', 'khdgj (49)', 'idjugav (99)', 'heuuqx (77)', 'yierd (96) -> ubnxkza, whlsvf, pnnpym, tznsg', 'yciccp (173) -> ijpsv, fjtafl, lxwntcm, saacvs', 'jcekn (38)', 'boxtod (126) -> sxtbzfe, etdah', 'iunue (25)', 'iceaj (216) -> zbqgiy, taxdaf', 'vobnuq (64)', 'grkyj (7)', 'etgjaum (61)', 'erjcx (47)', 'sqcodst (19)', 'vimzk (67)', 'gldkli (29)', 'yikzq (164) -> yhrnh, yipnm', 'aqksi (155) -> olotqeb, vioyx', 'wkjhmcd (33)', 'awsdwry (14)', 'dgehtvc (191) -> sxwcr, usfkacz', 'ohprzku (5)', 'aztstf (32)', 'grrbzan (61)', 'spcyi (23)', 'olntlo (299)', 'qczgjc (26)', 'svdlp (11)', 'ormhqr (83)', 'wfnox (15)', 'hqwdr (19)', 'cwoyko (138) -> uycwnb, pttvms, ingae, tedoj', 'dgeseao (64)', 'iejyzgu (97) -> lgnfrti, lomvf', 'eqxumuo (44)', 'vqpkne (11)', 'gmpoe (164) -> gpxhd, deylq', 'yhxkh (185) -> vyabn, xtwaov', 'ugeudg (68) -> dxffsoq, nyzvofv, tvrosaa, nmojt', 'wfuoll (1715) -> cciwzc, qpafkjx, axlitg', 'xmbafj (44)', 'xvpopw (58) -> wkhzk, zlnks', 'tcawlkc (38)', 'nddekdg (57)', 'jtejd (16) -> fzklxq, jrbqu, qhxns, lerqv', 'vyybi (86)', 'arhlwh (90)', 'ffizjl (84) -> szeszcp, wgmvio', 'bmwankt (71) -> tdmok, ygkwtl, sgose, uohurz', 'viantn (67)', 'qnqwt (14)', 'pcpcm (36)', 'orpzr (57)', 'ttfdct (37)', 'xjsyk (217) -> zhjzpaa, qylvdk', 'wiqpx (75)', 'pfyexc (252) -> zzqjykw, alflnz', 'rhifo (66)', 'lerqv (68)', 'pohqjzd (103) -> qltdz, ppzlmxg', 'scqhs (61)', 'vcgyi (391)', 'whlsvf (40)', 'edyfj (85)', 'jpvyg (82) -> lhbmgxc, qtxkvx, kynyas, easamud', 'jjwadjm (32)', 'lomvf (40)', 'snxgfl (148) -> ypufgmt, qvtwlq', 'gqxhfjz (85)', 'vzpkp (24)', 'ddkhuyg (57) -> alywuv, nvdoenr, mnyng, rhsztrd', 'iouamne (10)', 'tnkptkm (45)', 'xxqwea (82)', 'comyzns (69) -> fcmnfq, nrzhlvo', 'liwwgd (12)', 'nfbcs (185) -> vzpkp, wmfydk', 'kmoov (7)', 'yoabvhm (78)', 'tiwxhoa (107) -> wfnox, bwdijxn', 'tedjgv (5)', 'pqeph (56)', 'slqmpe (35)', 'wbntjyi (81)', 'pgmnqws (11)', 'indhpfx (163) -> umlbvg, fjdki, ctjygk', 'cokjdc (54)', 'bzapqu (76)', 'etevb (52)', 'dlluqgz (89) -> asdbbxb, vfetz', 'cxqdrz (17)', 'mynuy (249)', 'lgtpuqr (102) -> cdooel, eozsgq, dfsas, ldbwwt', 'iqcjr (27)', 'ythoww (176) -> alqkr, qicxdmg', 'ykshd (464) -> qufymlj, simlhnw, kjljvr', 'bqzfjn (609) -> txywrwk, tpvcmkz, fklkig, katovn, jgckfb, vwqquk', 'kywxkgm (96)', 'vzpwamg (84)', 'mgqfs (10)', 'zdljb (193) -> wviisf, zhavocr', 'sqdhc (79) -> cwoyko, pfyexc, mdyhk, zscqv, eqpuq, zspohe', 'zznkz (51) -> vyybi, sblacv', 'elvsrz (38)', 'xvgcls (73)', 'eylfls (71)', 'qrjor (13)', 'gqmls (40973) -> fqvvrgx, szmnwnx, jfdck', 'oprsej (181) -> rpijkf, wtosgg', 'ejkxeg (29)', 'mqccum (47)', 'zhjzpaa (20)', 'wsqlsgl (94)', 'zdncj (15)', 'xttsj (29)', 'zjzkwxq (92)', 'hlsoglk (6)', 'srbczq (70)', 'rvzjawx (54)', 'rkgvdhv (83)', 'pnnpym (40)', 'atzcjm (75)', 'optohy (43)', 'jsuevqz (5)', 'xdraxfj (16)', 'hlkvwq (216) -> wiqpx, bhxtgro', 'wgapb (7)', 'fyrauka (35)', 'kzeubgd (270) -> wwritm, wrcpxdx, kxouhtb', 'hughxts (215) -> asxiywb, dzwnzm', 'kvvjhrt (155) -> zsajqjv, nvcmjx, qczgjc', 'goaazlt (8)', 'errrzm (249)', 'kuhyqad (66)', 'gwohx (93)', 'kocwei (16)', 'yftqma (91) -> fewgbm, cukwe', 'katovn (559) -> ffizjl, ondvq, nbbctar, aonrg', 'rrrxeic (240) -> gwwxkxx, aeljb', 'vuldvce (107) -> mdoyb, hukfj', 'uwaxli (79) -> ortan, hlglt, oivlxe, eilfrxc', 'zsnenc (33)', 'pjzyj (48)', 'fewgbm (80)', 'igiqnkc (242) -> idjugav, cwkqb', 'xvteib (12)', 'ykhrxqf (54)', 'fjtafl (12)', 'syrnxgz (152) -> flzcf, rblzgyw, yzkzx', 'ztxam (5)', 'qzoas (13)', 'iolil (49)', 'fqisabu (50)', 'dismcam (76)', 'phwddnu (84)', 'nmojt (58)', 'txmdxj (94)', 'omkgoai (71)', 'dyamtle (33)', 'kqawctp (93)', 'klkodi (93) -> edyfj, wtsesxe', 'bpzwq (56)', 'ldwogg (76)', 'enswibe (379) -> hlsoglk, nkpzu', 'nmfsbu (24)', 'lybjgk (82)', 'cjxuj (30) -> gtjgxiw, wxksnf', 'bzbyqoq (39)', 'deylq (83)', 'owprin (97) -> komav, zzdvozt, eordj', 'rblzgyw (22)', 'bymyuke (511) -> dadlbnn, htwkr, dlluqgz', 'szsfe (45)', 'tedoj (47)', 'arjsnz (70) -> rwrusdg, krgdzw, olhbx', 'fkagf (88)', 'imuupp (7)', 'ghebwaz (15) -> xxqwea, lybjgk', 'obbei (215) -> jsuevqz, hxsuo', 'pnctz (5)', 'cxgxbo (44)', 'ivqduu (15)', 'qzuirrb (55)', 'rdihhfv (408) -> ozjka, mskbq, qrpis, dqury', 'hhivpic (78)', 'emdnkj (81)', 'hhdth (356) -> ylixmj, ukgzz', 'jovgiy (96)', 'cvkec (71)', 'sgaefd (93)', 'bkomu (19)', 'effjvcu (89)', 'ayvcc (43)', 'ocmuu (109) -> pbjuhpo, ovlbvyj', 'sxbee (32) -> fplzsya, yftqma, hweub, yhxkh, xhymdo, cafxx', 'llbsax (97)', 'ylfgaps (217) -> tzbreu, izxgcf', 'qhxns (68)', 'ymheeao (52)', 'qzzhap (127) -> uhyboog, nzlhfa', 'mskbq (191) -> hqwdr, askqu', 'fhlbjvx (73)', 'wcwqeyz (17)', 'crlgf (203) -> cxqdrz, kjtdypr', 'ngvqne (83)', 'jjeci (43)', 'lurly (16)', 'klzgol (52)', 'ctjygk (43)', 'sjyso (72) -> usbjn, puuwu', 'wustjt (7451) -> quinb, sqdhc, kcekden', 'rlsnxvu (628) -> xdkin, wnvmb, tfrjlk', 'wnmbn (13) -> egoezf, nodgjd, vrrmn, uicpy', 'hqmxuv (23)', 'rnhom (20)', 'ifmgil (81)', 'nmmxms (68)', 'bryrofn (35)', 'fixbeu (46)', 'ebfzjux (53)', 'nnoaqvv (433) -> isixko, frklhh, ugeudg', 'nyzvofv (58)', 'czgov (32)', 'gpkltyi (95)', 'ortan (34)', 'ylmixxx (17) -> ewycyf, iddby', 'uaxhb (91)', 'pqjrycz (117) -> urjsyac, olwudc, ezntvw, gpktinr', 'igrih (240) -> cdahg, vqpkne', 'ifajhb (36753) -> thuzqqo, fwlspf, mhfci, bbeclr, arjsnz', 'hipirzc (989) -> vpmtex, hhzjn, oilsjpr, mpxfrig, geibkdq, xzjdfbr', 'mqgculh (73) -> yvchtk, zmiee', 'msjeeks (333) -> tqclz, fjayhh', 'nkpzu (6)', 'jgckfb (568) -> bcjpkwf, ungcoot, mzhyo, iwcpvdx, dvuug', 'cwkqb (99)', 'zanpviw (57)', 'qkzklgx (37)', 'wdycxsw (246) -> gzokm, yqpxoki', 'sskog (64)', 'ucqru (52)', 'ipruxk (39)', 'bbvrbl (45)', 'idgmre (15)', 'tcclaa (221) -> wdblza, vfdnvk', 'xybhge (66)', 'sgose (32)', 'tzcymqj (28)', 'jzjxhyw (153) -> krovuvc, brolhd', 'ixlern (201) -> llzodgr, hwdtq', 'ahuboc (173) -> jkszke, lpxleg', 'xnxcez (94)', 'kynyas (71)', 'ylixmj (7)', 'jnojpf (54)', 'qicxdmg (29)', 'xwmjpb (96) -> eqxumuo, xmbafj', 'gqzczp (27) -> bzapqu, dismcam', 'zwxjsev (33)', 'ypvews (69)', 'cdooel (34)', 'zwaky (53) -> dqcxe, ojyssxz', 'ovomgd (8)', 'fzklxq (68)', 'vjvjnc (988) -> hoyipx, qoxsu, comyzns', 'efehrqd (11)', 'ghqvymr (12)', 'kcvhi (39)', 'hrpzu (179) -> rlhqosc, bryevj', 'zknbqr (35)', 'dcibpv (30)', 'kndpli (186) -> gegrzz, vandhv', 'iiurfqv (62)', 'ovvmrux (304) -> ulvoyev, lgkrhh', 'errip (22)', 'zjxspcp (1244) -> tiwxhoa, pqjrycz, sdstw', 'gwwxkxx (11)', 'yziwzua (70)', 'cczfm (749) -> pnghx, tusimd, putdqt, sbcyifk, uxblgk', 'alywuv (81) -> mlhga, odzzie, awddb, koxzwq, cczfm, hipirzc, qqktjg', 'corqny (57) -> crlgf, xkfuz, gzoyqay, cakpt', 'cqdkb (99)', 'atkstsn (57) -> kntyjf, hwcwcn', 'jfdck (65) -> marnqj, moxiw, sxijke, ojgdow, fnlapoh', 'afjqx (115) -> unokgle, bwsvr', 'mdoyb (57)', 'upair (102) -> xfxqbqv, svdlp, hqget', 'sdstw (73) -> czgov, tgrtt', 'vlcrx (61)', 'ymrfvp (203) -> veplkeo, iouamne', 'vtlxs (92)', 'wxakaqf (253) -> xnpbhpt, liwwgd', 'qigsvd (218) -> gmpoe, ymqmr, wdycxsw, ixszebq', 'joyncgz (73)', 'saxamw (30)', 'vyabn (33)', 'fafvyk (62) -> egjsilp, usodp', 'uigot (69)', 'myhfh (9816) -> howpl, upvrm, xjsyk', 'kfohhmp (81)', 'rirch (72)', 'bzjze (94) -> wsjuynd, aicwnq, fixbeu', 'hzrphej (74)', 'ozjka (229)', 'ppkxgj (62)', 'zgmrmd (167) -> sebtdcx, nmfsbu', 'mtgsssx (96)', 'ruxqapz (66) -> xhhtjwu, xhirm', 'cwrllq (91)', 'cpwxm (22)', 'lsxnn (232)', 'lijnzj (5)', 'eozsgq (34)', 'uohurz (32)', 'rklnuv (41)', 'tgrtt (32)', 'umyqf (89)', 'txywrwk (787) -> lbflpug, indhpfx, sxcxmg', 'ttbtij (22)', 'uohmo (432) -> zznkz, ustkg, stflbsr, qzeljtb', 'qowagej (82)', 'ingae (47)', 'lpxleg (32)', 'moxiw (184) -> cqtkhqi, pohqjzd, oagvuu, nfbcs, hughxts, kvvjhrt, qzzhap', 'puuwu (47)', 'oywnenv (245) -> fhlbjvx, joyncgz', 'deiso (34)', 'pnghx (158) -> wktjf, umyqf', 'nuyake (5)', 'sxtbzfe (68)', 'elhjwu (54)', 'mbsaywb (38)', 'hcetpw (99)', 'idcgo (52)', 'uosltv (86) -> wxmxkzn, xvgcls', 'cqtkhqi (233)', 'wkhzk (88)', 'qdxvydf (70)', 'alicosg (52)', 'hwcwcn (94)', 'cxqgvb (41)', 'nthusc (80)', 'elxydx (145) -> orpzr, nddekdg', 'chpjfv (83) -> psyino, hivoik, qhqbqj, qzuirrb', 'wmfydk (24)', 'uusufw (74)', 'tzbreu (41)', 'abmlupq (49) -> fcpejj, qgiijpu, iolil, khdgj', 'qfitmrm (23) -> tmgoed, gkhrgd, zjzkwxq, bjcthpx', 'ygkwtl (32)', 'qclhx (79)', 'hgyelhc (7)', 'riogbaf (5)', 'uhyboog (53)', 'qoxsu (189) -> qzoas, jedlbro', 'iakgro (52)', 'koxzwq (1633) -> geuopn, ransdtt, bmwankt, qmdbgke', 'fwkxcq (89)', 'sqauq (218) -> paquh, goaazlt', 'walei (418) -> wipafb, rzpxffj', 'mflvlww (51)', 'yzvvyb (144) -> eyiiwv, awaoi', 'uspzk (173) -> idcgo, etevb', 'kbtfnu (34)', 'mpuhqjm (78)', 'krbsvt (17)', 'xdkin (59) -> gkzbah, cxgxbo, jdvbztj, mviyuy', 'rtngius (83) -> boxtod, wpwlg, igrih, tgxuhxp, iceaj, kqecnz', 'vpemk (5)', 'wtosgg (59)', 'dgoocsw (99) -> ifajhb, gqmls, sgmbw, ddkhuyg, rhqocy', 'paquh (8)', 'zsajqjv (26)', 'vuknf (55)', 'zzdvozt (45)', 'rgonoq (33)', 'vlglq (98)', 'wsrmfr (6) -> optohy, tcxwrcv, wbckbcz', 'vpmtex (240)', 'wnvmb (79) -> hhivpic, pikqy', 'unllgjg (38) -> dgeseao, vobnuq', 'smbaw (89)', 'bpgbauh (48)', 'isixko (284) -> kkuzi, ssdpo', 'mgghj (61)', 'anraget (52)', 'kqecnz (262)', 'uqgco (161) -> uwuouhv, ocmuu, uvogit, mvwcdq, errrzm, mynuy', 'gpktinr (5)', 'xmhil (37) -> wloqry, gzrmt, gmktbew', 'howpl (191) -> qlkhbf, rnqtg', 'pozhxfb (81)', 'twpxg (20)', 'ransdtt (135) -> suriq, vqbaw', 'olotqeb (52)', 'szmnwnx (3808) -> mgayiu, nnoaqvv, kupsxf, rlsnxvu', 'gvtnin (171) -> awgucd, krqff, ipruxk', 'yquhjrb (59)', 'xcrmvq (57)', 'uhuieb (27)', 'yqkwau (99)', 'kkszxy (9)', 'fvtmh (118) -> neltlwg, irzscv', 'nzlhfa (53)', 'aqfjqh (47)', 'uqraz (93)', 'alqkr (29)', 'mnyng (12185) -> plvjk, vjvjnc, clxlfgu', 'qbvurh (86)', 'emsacsk (161) -> jcekn, tcawlkc', 'mlhga (83) -> qfitmrm, enswibe, tefmun, qshflsm, vcgyi, oywnenv', 'rmvdiwr (15)', 'zlnks (88)', 'zmiee (35)', 'bmswiwx (37)', 'dapjjl (26) -> pbxzzdi, elxydx, ghlkk, rnjqmh, dgehtvc, aqksi', 'jfhqmi (61)', 'fiehsiq (71)', 'zbqgiy (23)', 'ssdpo (8)', 'mdyhk (326)', 'tefmun (391)', 'rzned (54)', 'uhalup (15)', 'nodgjd (195) -> feygolx, mtgsssx', 'plevjup (190) -> kmcjs, vtwtgf', 'nqkpd (7)', 'srhcew (39)', 'fjdvux (95)', 'fqvvrgx (8363) -> xmhil, dbzwyez, bmhlcgg', 'askqu (19)', 'jlsxjq (162) -> zanpviw, xcrmvq', 'kbjpgv (71) -> atzcjm, vldxx', 'kntyjf (94)', 'awddb (1643) -> npsuo, rrrxeic, fhyfd', 'aonrg (52) -> fyqlzxt, ehhlvc, bpzwq, qeoicwx', 'nconokw (45)', 'qsgkmc (28)', 'qxubki (10)', 'nepmits (19)', 'krzuab (135) -> jtxsofx, xrockzz', 'hwvnv (83)', 'gmktbew (74)', 'wdblza (21)', 'ijpsv (12)', 'ainqphn (45)', 'zwwrwfy (9536) -> fquyicp, sbxkokp, corqny, kzeubgd', 'yjlzpv (198) -> jshaf, vzpwamg', 'vqbaw (32)', 'xnpbhpt (12)', 'zlmvme (234)', 'fhyfd (154) -> tevxh, cpphf', 'easamud (71)', 'mgayiu (93) -> ksvdw, euueza, txfnjo, bhtwp, pvnjsr', 'tgqnyb (8591) -> rtngius, uqgco, zjxspcp', 'ixszebq (140) -> atfgzcb, fjdvux', 'ymjxuy (67)', 'veplkeo (10)', 'whgqhb (91) -> nqehtaf, wnshgr, wfuoll, cmnjg, olqgu', 'jlryq (54)', 'nyaqnau (79)', 'uwuouhv (215) -> pwguzgm, krbsvt', 'ogpunov (34) -> eqsrff, uwaxli, tszcogp, zgmrmd, wugret, zdljb', 'efajqe (70)', 'obvvk (29)', 'tfpjxcv (52)', 'gtjgxiw (80)', 'egoezf (373) -> kmoov, hgyelhc', 'sxwcr (34)', 'geibkdq (148) -> oaqtjz, nwcbnxq', 'yirmii (27)', 'ifdeve (25)', 'ouxdvp (202) -> gbrqt, edncj', 'isbppt (92) -> rkgvdhv, hwvnv', 'bajtat (252) -> wsqlsgl, ykohs', 'aofkt (84)', 'zbgjuk (84)', 'ondvq (122) -> wthxapy, vqghnm', 'fzerj (83) -> feuirvn, rklic, vxbzw, rzvrn', 'etdah (68)', 'jjwpqn (20)', 'xykcof (1152) -> ptmqqpk, zfotzg, jfhqmi, kivlu, vvkgsba', 'dlzlo (75) -> viantn, ymjxuy, vimzk', 'sdiyd (25)', 'krgdzw (70) -> oxvcp, sdllj, jtejd, fjiemrs, gvtnin, dfnijm, yzvvyb', 'exuelye (57)', 'ymfjt (19)', 'jtxsofx (37)', 'oagvuu (79) -> heuuqx, meqbgw', 'kthzxmf (23)', 'kuqnndb (57)', 'gtdfvuu (56)', 'wktjf (89)', 'mpxfrig (78) -> elhjwu, cokjdc, rvzjawx', 'etdmt (35) -> emsacsk, emvml, egcyvrv, srjbcye, ffyfj, ahuboc', 'psblh (90) -> kfhcuvf, uspzk, wxakaqf', 'tobzv (440)', 'futsmzx (333) -> efehrqd, hmfyf, pgmnqws', 'ubnxkza (40)', 'kesgd (54)', 'hhzjn (116) -> npmafis, ppkxgj', 'cxthvz (20)', 'tdmok (32)', 'wsuihj (61)', 'gkpgf (19)', 'ncqiou (38)', 'gwgdt (47)', 'qufymlj (241) -> bbvrbl, ainqphn', 'zscqv (188) -> acvrb, ggplfue, iygtv', 'zzqjykw (37)', 'xtwaov (33)', 'acvrb (46)', 'qbdhk (51)', 'fjuudqb (37)', 'kxolyhi (29)', 'evgupeo (91)', 'marnqj (1283) -> upair, mkrrlbv, vqkwlq, wsrmfr', 'ssbjh (130) -> vfzlh, tdrsmxa', 'wlefwf (30)', 'tbute (89)', 'diupl (79)', 'dadlbnn (99) -> qrpab, jejvld', 'yipnm (37)', 'ymqmr (66) -> xcqhk, yxcliv, dubsgvx, kuhyqad', 'nldgsz (68)', 'hlglt (34)', 'nrzhlvo (73)', 'kxpffcy (27) -> cqdkb, hcetpw, yqkwau', 'lhbmgxc (71)', 'ehhlvc (56)', 'fwxtdml (156) -> wfzbtxa, mygjnz, pqeph', 'dbzwyez (195) -> mcvws, kocwei, lurly, xdraxfj', 'jipgo (772) -> qgptpig, klkodi, tcclaa', 'atfgzcb (95)', 'sbcyifk (336)', 'jdfrbhy (48) -> sgrwrkz, czfza, ymheeao, ucqru', 'mohhap (7)', 'raormr (23)', 'fyqlzxt (56)', 'eodyisb (11)', 'wchwgnd (62)', 'thuzqqo (1588) -> dapjjl, lvbjtf, bijhyzu', 'xqukn (79)', 'mmdrry (21) -> gwgdt, hiwslh, erjcx, mqccum', 'efsbeb (245)', 'vwltm (40)', 'ixrrfy (48)', 'sfbpnnz (41) -> cwrllq, evgupeo', 'mjvopd (59)', 'vjeiie (54)', 'sblacv (86)', 'tmgoed (92)', 'iddby (63)', 'asxiywb (9)', 'qmdbgke (155) -> ttbtij, cpwxm', 'wpdwdep (90)', 'wbckbcz (43)', 'wenper (45)', 'emvml (47) -> vipgc, gpkltyi', 'xvtwfks (14)', 'kzpml (81)', 'yqpxoki (42)', 'xcqhk (66)', 'pbxzzdi (127) -> rgonoq, zsnenc, zwxjsev, dyamtle', 'auulu (68)', 'jedlbro (13)', 'welid (17)', 'sbxkokp (341) -> gxzgsaa, sjyso, snxgfl, unllgjg', 'gybgrld (51)', 'jmazezm (32) -> grrbzan, hxnnsp, etgjaum, wccpr', 'tusimd (260) -> rfrgmgz, mbsaywb', 'mqhwlq (8)', 'ydurwqb (43)', 'fyeqds (93)', 'dhhpxsj (55)', 'upvrm (79) -> effjvcu, uwrqxmj', 'bhtwp (65) -> scqhs, sixicw, mgghj', 'fcpejj (49)', 'awaoi (72)', 'ahqlq (23)', 'dqcxe (84)', 'kddvj (23)', 'usbjn (47)', 'izxgcf (41)', 'bqfsjz (86) -> ldwogg, mbvjj', 'sxijke (987) -> dlzlo, jlsxjq, jmazezm', 'ulvoyev (33)', 'cpphf (54)', 'qfanlc (11)', 'kqtmc (83)', 'hiwslh (47)', 'mviyuy (44)', 'hgyyml (91)', 'fquyicp (113) -> fudpn, sfbpnnz, ymrfvp, fyptb', 'xvawgcm (62)', 'suriq (32)', 'tfrjlk (235)', 'dfnijm (168) -> saxamw, sgwcf, wlefwf, dcibpv', 'xrockzz (37)', 'zeximw (81)', 'rckuzt (97)', 'gvtzws (35)', 'dlqmd (81)', 'fjcibi (84)', 'foldo (31) -> skyucv, ncunr', 'gvzze (70) -> mupwbp, qowagej', 'zgrdyl (96)', 'rpijkf (59)', 'drdvm (37)', 'wxksnf (80)', 'ungcoot (161) -> ejijju, gldkli', 'pvnjsr (228) -> tedjgv, vpemk, lijnzj, ohprzku', 'lgnfrti (40)', 'ryrtqj (73) -> fvtxd, vuknf, dhhpxsj', 'npznojo (47)', 'usfkacz (34)', 'vandhv (24)', 'hoyipx (119) -> rpqvli, ixrrfy', 'tevxh (54)', 'bvrarwr (12)', 'mxukll (22)', 'ytbnpd (5612) -> rdihhfv, ctdey, vetgu, bymyuke, ogpunov, uohmo', 'feuirvn (64) -> yjlzpv, mibwe, hlkvwq, ufses, jpvyg, auzdz, futsmzx', 'oaqtjz (46)', 'srjbcye (181) -> xvtwfks, skwbfku, qnqwt, awsdwry', 'bjcthpx (92)', 'xmiygp (35)', 'tszcogp (189) -> abzdsbs, qrjor', 'cklbsi (71)', 'npmafis (62)', 'ksvwjw (31) -> pcuxhb, zigfjrn', 'pluph (15)', 'tggyn (80)', 'yrdpurl (30)', 'igjmhxe (23)', 'bkzzc (258)', 'hmfyf (11)', 'klvncy (98) -> slqmpe, kbyrlz, xzjiiwl', 'hscywgt (61)', 'ilsqjz (285) -> nqkpd, grkyj', 'ksvdw (120) -> sskog, xettl', 'wpwlg (86) -> kuxclnz, fkagf', 'gkzbah (44)', 'qtxkvx (71)', 'xiksvn (114) -> cklbsi, ydhrzjf', 'fjrrlug (16)', 'rzpxffj (11)', 'wviisf (11)', 'waoiyzo (23)', 'dtyaj (184)', 'gbcnx (64)', 'xtwtv (83)', 'lsppdni (22)', 'ydhrzjf (71)', 'clxlfgu (86) -> yciccp, lhhlg, zwaky, kbjpgv, vuldvce, jzjxhyw, crxuc', 'wccpr (61)', 'zqkgqs (126) -> obvvk, ejkxeg', 'ufses (326) -> jjwpqn, rnhom', 'emdtn (87)', 'kbgfqwc (70)', 'yzkzx (22)', 'pkeua (68)', 'jdvfkii (69) -> qdibw, fthyzq, kdcijis', 'twxwtr (47)', 'ojyssxz (84)', 'tvrosaa (58)', 'rhsztrd (12713) -> etdmt, ykshd, xykcof', 'hvjgdxs (43)', 'fklkig (1573) -> ykcmvla, owhxvku, yrdpurl', 'ejijju (29)', 'hfgokdn (85)', 'yxljri (103) -> ttfdct, jshxbra', 'ykavsf (7)', 'tkpcmi (32)', 'ovlbvyj (70)', 'fmvdadz (107) -> opqpgol, bryrofn', 'urjsyac (5)', 'jejvld (86)', 'ygbecwq (85) -> mjvopd, midqcpz', 'pttvms (47)', 'xzjdfbr (176) -> jjwadjm, tkpcmi', 'kxsweg (43)', 'kmcjs (22)', 'fqqzx (669) -> fafvyk, syrnxgz, xofjd', 'dvuug (45) -> nxtmr, emdtn', 'xhhtjwu (83)', 'sebtdcx (24)', 'xxiymn (110) -> ryrtqj, yikzq, fvtmh, bqfsjz, lgtpuqr, diila', 'onwqbz (177)', 'ffyfj (199) -> nepmits, sqcodst', 'kdmuzrx (90) -> efhuz, yziwzua, wxnoy, kbgfqwc', 'coxtcw (153) -> jdfrbhy, orulm, xiksvn', 'avsoisf (81)', 'aicwnq (46)', 'fudpn (87) -> nldgsz, oluzb', 'ozizlok (21) -> kfohhmp, dlqmd, zbbdyc, qlrcubm', 'yrmifh (11)', 'hxsuo (5)', 'zfmqgun (85)', 'htwkr (73) -> rhifo, xybhge, slhmny', 'kzzedp (81)', 'ocobkpo (322) -> yquhjrb, akmjes', 'kzupr (72)', 'frklhh (256) -> qfanlc, ouuud, gamlcl, chlyf', 'alflnz (37)', 'xettl (64)', 'vfzlh (63)', 'pcmimkt (19)', 'mcvws (16)', 'ezntvw (5)', 'nqehtaf (1857) -> vkmtnn, iouczne, krzuab, mmdrry', 'bbeclr (1645) -> zwqgf, wnmbn, jipgo', 'ompzpgp (290) -> uemklxf, vwltm', 'mbvjj (76)', 'kbyrlz (35)', 'adwzzi (71) -> yirmii, pptok, iqcjr, uhuieb', 'fplzsya (201) -> ifdeve, sdiyd', 'qrpis (19) -> srbczq, efajqe, qdxvydf', 'qdibw (78)', 'ouuud (11)', 'wohob (108) -> drdvm, mdbzm, bmswiwx, fjuudqb', 'lbflpug (252) -> mgqfs, bpknup, qxubki, bbijzr', 'xeyfy (51)', 'mohbkpv (81)', 'szeszcp (96)', 'myeqz (50)', 'jmbptp (11)', 'quinb (1927) -> jnojpf, qtzor', 'xkfuz (75) -> rzned, eyqkgna, vjeiie', 'kasnq (96)', 'npsuo (10) -> phwddnu, zbgjuk, aofkt', 'uvogit (93) -> alicosg, iakgro, aujqr', 'zgbzqf (21) -> dunscc, qndcql, bzbyqoq, srhcew', 'xqvmqe (198) -> gyrgr, kkszxy, mourke', 'boipij (116) -> vtlxs, uyzpz', 'gzokm (42)', 'ppzlmxg (65)', 'hukfj (57)', 'wnshgr (1978) -> avzxg, afjqx, mqgculh, ylmixxx, pzxfm', 'mvwcdq (149) -> myeqz, fqisabu', 'komav (45)', 'lgkrhh (33)', 'gpxhd (83)', 'zwqgf (661) -> obbei, bxdxjoa, xqvmqe, pcqhhy', 'bbijzr (10)', 'wcsnr (39)', 'dubsgvx (66)', 'pmakzzf (129) -> funtwzh, lccukr', 'funtwzh (24)', 'vqkwlq (111) -> bvrarwr, ghqvymr', 'czfza (52)', 'xieqyy (89)', 'nbbctar (96) -> wpdwdep, arhlwh', 'ykohs (94)', 'nvdoenr (14321) -> coxtcw, psblh, foyabk', 'sdllj (260) -> mzbhs, wgapb, ykavsf, mohhap', 'bwdijxn (15)', 'skyucv (73)', 'jshxbra (37)', 'krivqx (35)', 'fthyzq (78)', 'ghlkk (73) -> kqawctp, sgaefd', 'pcuxhb (53)', 'zdofuei (83)', 'qiutta (15)', 'fvtxd (55)', 'bhxtgro (75)', 'vqghnm (77)', 'dnivyr (64)', 'qltdz (65)', 'wiqsy (156) -> kzupr, rirch', 'uicpy (387)', 'awpyosw (14) -> smbaw, xieqyy, tbute, fwkxcq', 'stflbsr (190) -> yrmifh, eodyisb, jmbptp', 'bcjpkwf (15) -> auulu, eeqoiz, nmmxms', 'iieig (101) -> elvsrz, ncqiou', 'exqhrl (61)', 'tqclz (6)', 'eyiiwv (72)', 'feygolx (96)', 'gkgka (21) -> xnxcez, txmdxj, yqlduph', 'tznsg (40)', 'flzcf (22)', 'rhqocy (36632) -> fzerj, myhfh, bqzfjn', 'lhhlg (111) -> wjsijg, szvfc', 'jshaf (84)', 'efhuz (70)', 'qtzor (54)', 'imeyrl (23)', 'vrrmn (47) -> gqxhfjz, hfgokdn, zfmqgun, dljfl', 'egcyvrv (132) -> cdkadkn, gvtzws, zknbqr', 'qgptpig (177) -> jjeci, dpvwrn', 'kjljvr (15) -> qclhx, xqukn, nyaqnau, diupl', 'euueza (146) -> xeyfy, gybgrld', 'kupsxf (724) -> zxtwo, klvncy, ygbecwq', 'rfrgmgz (38)', 'vxbzw (1698) -> uosltv, bzjze, owprin, lsxnn', 'pptok (27)', 'vipgc (95)', 'gzoyqay (141) -> pjzyj, bpgbauh', 'kjtdypr (17)', 'mhdhb (86)', 'zxtwo (135) -> ckaqw, ovcxkye', 'lvbjtf (1466) -> kuqnndb, exuelye', 'vfdnvk (21)', 'pzxfm (107) -> xvteib, gookalb, rpaudj', 'ubxume (68)', 'dljfl (85)', 'tfmvb (128) -> vlglq, kcscgb', 'zspohe (78) -> jkfnrik, iiurfqv, wchwgnd, xvawgcm', 'uycwnb (47)', 'rwrusdg (1351) -> atkstsn, efsbeb, abmlupq', 'gbrqt (16)', 'hxvizze (85)', 'kcscgb (98)', 'iwcpvdx (161) -> kxolyhi, xttsj', 'pnmkw (190)', 'zhavocr (11)', 'eyqkgna (54)', 'rnqtg (33)', 'llzodgr (5)', 'bmnsk (17)', 'rwaeimg (137)', 'putdqt (78) -> qbvurh, rbauepa, mhdhb', 'meqbgw (77)', 'cwahmsr (56)', 'endpyd (97)', 'wgmvio (96)', 'mdbzm (37)', 'aeljb (11)', 'tcrpymd (97)', 'owhxvku (15) -> pnctz, riogbaf, qrpgt', 'pwguzgm (17)', 'ihwkjjt (16)', 'eqsrff (33) -> hgyyml, uaxhb', 'rpaudj (12)', 'cdahg (11)', 'gwgas (54)', 'gzrmt (74)', 'kuxclnz (88)', 'ffdxovh (25)', 'geuopn (13) -> fyeqds, uqraz', 'umlbvg (43)', 'gamlcl (11)', 'ywnji (37)', 'aezwvo (146) -> ayvcc, kxsweg', 'xqdih (23)', 'pbjuhpo (70)', 'qltdv (32)', 'irzscv (60)', 'kdcijis (78)', 'olwudc (5)', 'rbauepa (86)', 'kcekden (1504) -> pmakzzf, fmvdadz, zgbzqf', 'olczth (39)', 'hxnnsp (61)', 'psyino (55)', 'vkmtnn (139) -> augxmyy, fyrauka', 'edncj (16)', 'bryevj (83)', 'vlisesb (39)', 'ykcmvla (20) -> cvgoojy, codttfw', 'wgnoil (79) -> vpmywt, xjekui, gtdfvuu, cwahmsr', 'gookalb (12)', 'aujqr (52)', 'fjiemrs (220) -> wcwqeyz, welid, sytip, bmnsk', 'avzxg (7) -> pkeua, ubxume', 'vwqquk (25) -> ythoww, sqauq, plevjup, ouxdvp, qtbnqo, kndpli, gvzze', 'usodp (78)', 'qpafkjx (71) -> hxvizze, klvufp, txwsp', 'stttgb (13)', 'lxwntcm (12)', 'vpmywt (56)', 'gyrgr (9)', 'rpqvli (48)', 'fcmnfq (73)', 'ovcxkye (34)', 'sgrwrkz (52)', 'yejoqrc (16)', 'qeoicwx (56)', 'txfnjo (140) -> gwgas, jlryq', 'ioyiklx (120) -> uigot, ypvews', 'hwdtq (5)', 'wjjsgvw (74)', 'fwlspf (176) -> qpoodx, sxbee, xxiymn, qigsvd', 'wwritm (245)', 'mzhyo (198) -> cxodl, aaecklm, imuupp', 'mcpcxw (61)', 'txwsp (85)', 'iyrapzn (84)', 'awgucd (39)', 'pbeegf (180) -> ztxam, nuyake', 'rklic (832) -> ylfgaps, gedajwo, olntlo, ilsqjz, tdqxy, oprsej', 'ypufgmt (9)', 'mourke (9)', 'wjsijg (55)', 'pikqy (78)', 'ckaqw (34)', 'wrcpxdx (83) -> avsoisf, kzzedp', 'xhirm (83)', 'rnjqmh (97) -> kzpml, emdnkj', 'oilsjpr (195) -> pluph, rmvdiwr, idgmre', 'qqktjg (1859) -> cjxuj, pnmkw, pbeegf', 'hqget (11)', 'qrpab (86)', 'vtwtgf (22)', 'vdpnz (158) -> qkzklgx, ywnji', 'hweub (201) -> vdebg, vcihirs', 'oluzb (68)', 'gegrzz (24)', 'tgxuhxp (262)', 'wxnoy (70)', 'jdvbztj (44)', 'mupwbp (82)', 'wtsesxe (85)', 'uwrqxmj (89)', 'orulm (128) -> dnivyr, gbcnx', 'vcihirs (25)', 'cdkadkn (35)', 'yvchtk (35)', 'yffid (143) -> deiso, kbtfnu', 'sytip (17)', 'qylvdk (20)', 'fyptb (100) -> gnbjv, rklnuv, cxqgvb', 'ldbwwt (34)', 'tcxwrcv (43)', 'zglws (56) -> kasnq, jovgiy, kywxkgm, zgrdyl', 'aikmwxj (173) -> bkomu, pcmimkt', 'chlyf (11)', 'oivlxe (34)', 'ggplfue (46)', 'bmhlcgg (103) -> yoabvhm, mpuhqjm', 'xlxct (137) -> twpxg, cxthvz', 'xzjiiwl (35)', 'krqff (39)', 'dunscc (39)', 'cxodl (7)', 'axlitg (234) -> imeyrl, waoiyzo, hqmxuv, spcyi', 'yhrnh (37)', 'mygjnz (56)', 'wloqry (74)', 'qndcql (39)', 'cmnjg (843) -> hhdth, ompzpgp, kdmuzrx, ovvmrux, awpyosw', 'pcqhhy (63) -> pozhxfb, mohbkpv', 'rlhqosc (83)', 'vioyx (52)', 'pegoi (27) -> qsjwlq, kxpffcy, fwxtdml, tfmvb', 'ljeztky (51) -> exqhrl, mcpcxw, hscywgt', 'lccukr (24)', 'brolhd (34)', 'plvjk (1222) -> ksvwjw, uglvj, rwaeimg', 'xfxqbqv (11)', 'gnbjv (41)', 'egjsilp (78)', 'vbkqzje (36)', 'simlhnw (223) -> kesgd, ykhrxqf', 'midqcpz (59)', 'tcwzc (33)', 'cakpt (29) -> anraget, tfpjxcv, klzgol, ntpmw', 'ncunr (73)', 'crxuc (176) -> qiutta, ivqduu, uvatphy', 'wipafb (11)', 'cukwe (80)', 'kxouhtb (181) -> aztstf, qltdv', 'wdjgdoh (51) -> ngvqne, zdofuei, kqtmc', 'uvatphy (15)', 'jkszke (32)', 'hivoik (55)', 'fjdki (43)', 'abzdsbs (13)', 'odzzie (1585) -> aikmwxj, yffid, qmhaa, ixlern', 'yqlduph (94)', 'mzbhs (7)', 'mibwe (162) -> qbdhk, mflvlww, vvwrg, nslyvt', 'wfzbtxa (56)', 'kivlu (35) -> hagdjuz, stttgb', 'szvfc (55)', 'uxblgk (230) -> lcfur, ebfzjux', 'hagdjuz (13)', 'slhmny (66)', 'qshflsm (361) -> uhalup, zdncj', 'oxvcp (232) -> ujupo, qsgkmc', 'jkfnrik (62)', 'qzeljtb (101) -> wsuihj, vlcrx', 'wugret (29) -> zrhyprz, gwohx', 'vvkgsba (61)', 'cafxx (152) -> zjzxav, tcwzc, wkjhmcd', 'otmpv (171) -> dopdknn, hvjgdxs, ydurwqb', 'eilfrxc (34)', 'mhfci (2359) -> pegoi, ubvvr, fqqzx', 'dqury (179) -> iunue, ffdxovh', 'gkhrgd (92)', 'bwsvr (14)', 'gedajwo (299)', 'dpvwrn (43)', 'vfetz (91)', 'dopdknn (43)', 'bxdxjoa (225)', 'qpoodx (1001) -> gqzczp, adwzzi, ghebwaz', 'fnlapoh (1284) -> yxljri, xlxct, foldo', 'mkrrlbv (43) -> ahqlq, igjmhxe, xqdih, raormr', 'bijhyzu (368) -> jdvfkii, chpjfv, wgnoil, gkgka', 'dfsas (34)', 'unokgle (14)', 'qsjwlq (268) -> tzcymqj, gtzrs', 'eordj (45)', 'tdqxy (77) -> hzrphej, uusufw, wjjsgvw', 'klvufp (85)', 'kfhcuvf (83) -> llbsax, rckuzt', 'vetgu (556) -> yierd, wohob, ssbjh', 'eqpuq (254) -> vbkqzje, pcpcm', 'zjzxav (33)', 'ustkg (57) -> ormhqr, xtwtv', 'ujupo (28)', 'vdebg (25)', 'skwbfku (14)', 'nslyvt (51)', 'cvgoojy (5)', 'qvtwlq (9)', 'iouczne (139) -> krivqx, xmiygp', 'foyabk (390) -> iieig, iejyzgu, onwqbz', 'kkuzi (8)', 'akmjes (59)', 'fjayhh (6)', 'bpknup (10)', 'zrhyprz (93)', 'olqgu (53) -> walei, bajtat, igiqnkc, tobzv, ocobkpo, zglws', 'xofjd (77) -> npznojo, twxwtr, aqfjqh', 'ptmqqpk (13) -> yejoqrc, ihwkjjt, fjrrlug', 'krovuvc (34)', 'tdrsmxa (63)', 'qmhaa (31) -> szsfe, nconokw, wenper, tnkptkm', 'sixicw (61)', 'sgwcf (30)', 'aaecklm (7)', 'ewycyf (63)', 'olhbx (1384) -> zlmvme, ljeztky, xvpopw', 'uemklxf (40)', 'nwcbnxq (46)', 'nvcmjx (26)', 'eeqoiz (68)', 'ntpmw (52)', 'qgiijpu (49)', 'iygtv (46)', 'jrbqu (68)', 'yxcliv (66)', 'codttfw (5)', 'wsjuynd (46)', 'dxffsoq (58)', 'sxcxmg (98) -> tcrpymd, endpyd', 'wthxapy (77)', 'sgmbw (613) -> ytbnpd, tgqnyb, whgqhb, wustjt, zwwrwfy', 'opqpgol (35)', 'zigfjrn (53)', 'tpvcmkz (1111) -> dtyaj, xwmjpb, zqkgqs', 'uyzpz (92)', 'ctdey (628) -> aezwvo, vdpnz, ruxqapz', 'gxzgsaa (88) -> wcsnr, kcvhi', 'rzvrn (1852) -> bkzzc, isbppt, ioyiklx', 'auzdz (82) -> fiehsiq, eylfls, cvkec, omkgoai', 'gtzrs (28)', 'diila (192) -> kthzxmf, kddvj', 'ojgdow (15) -> wdjgdoh, gwgnf, bzznyu, boipij, otmpv, wiqsy', 'saacvs (12)', 'qtbnqo (156) -> vlisesb, olczth', 'dzwnzm (9)', 'neltlwg (60)', 'qlkhbf (33)', 'xjekui (56)', 'lcfur (53)', 'augxmyy (35)', 'nxtmr (87)', 'cciwzc (158) -> fjcibi, iyrapzn', 'asdbbxb (91)', 'vldxx (75)', 'bzznyu (140) -> tggyn, nthusc', 'wxmxkzn (73)', 'gwgnf (57) -> wbntjyi, ifmgil, zeximw']
import re
finder = re.compile(r'^(.*) \((\d*)\) ?-?>? ?(.*)$')
def solve(data):
    on_who = {}
    carried = {}
    for line in data:
        if not '->' in line:
            continue
        m = finder.match(line)
        if m:
            carrying = m.groups()[2].split(', ')
            on_who[m.groups()[0]] = carrying
            for c in carrying:
                carried[c] = carried.get(c, 0) + 1
            
    return list(set(on_who.keys()) - set(carried.keys()))[0]
        
test_data = """pbga (66)
xhth (57)
ebii (61)
havc (66)
ktlj (57)
fwft (72) -> ktlj, cntj, xhth
qoyq (66)
padx (45) -> pbga, havc, qoyq
tknk (41) -> ugml, padx, fwft
jptl (61)
ugml (68) -> gyxo, ebii, jptl
gyxo (61)
cntj (57)""".split('\n')
assert solve(test_data) == 'tknk'
print(solve(data))
import re
from pprint import pprint
finder = re.compile(r'^(.*) \((\d*)\) ?-?>? ?(.*)$')
def get_base_weigths_tree(data):
    on_who = {}
    carried = {}
    weigths = {}
    for line in data:
        m = finder.match(line)
        weigths[m.groups()[0]] = int(m.groups()[1])
        if m.groups()[2]:
            carrying = m.groups()[2].split(', ')
            on_who[m.groups()[0]] = carrying
            for c in carrying:
                carried[c] = carried.get(c, 0) + 1
    
    base = list(set(on_who.keys()) - set(carried.keys()))[0]
    return (base, weigths, on_who)
def get_weigths(base, weigths, tree):
    if base in tree:
        q = [get_weigths(x, weigths, tree) for x in tree[base]]
        total = weigths[base]
        for e in q:
            total += e[1]
        if not len(set([x[1] for x in q])) == 1:
            print('problem in {}'.format(base))
            pprint(q)
            raise ValueError
        return (base, total, q)
    else:
        return (base, weigths[base])
def solve(data):
    base, weigths, tree = get_base_weigths_tree(data)
    pprint(get_weigths(base, weigths, tree))
    return True
test_data = """pbga (66)
xhth (57)
ebii (61)
havc (66)
ktlj (57)
fwft (72) -> ktlj, cntj, xhth
qoyq (66)
padx (45) -> pbga, havc, qoyq
tknk (41) -> ugml, padx, fwft
jptl (61)
ugml (68) -> gyxo, ebii, jptl
gyxo (61)
cntj (57)""".split('\n')
# assert solve(test_data) == 60
# solve(data)
data = ['um inc -671 if lbf != 5', 'j inc 236 if umr > -6', 'fk inc -246 if j < 241', 'uy dec -404 if mmw <= 2', 'j inc 372 if gk >= -1', 'uy inc -380 if umr > -4', 'dy inc 257 if es > -9', 'es dec 769 if es < 4', 't inc -429 if umr >= 0', 'hg dec 13 if dy < 267', 'is inc 66 if fk == -246', 'fk inc -30 if es > -775', 'ada inc 258 if umr > 3', 'eri inc -950 if lx > -4', 'umr dec -789 if x >= -4', 'um inc -783 if aao > -7', 'j inc -97 if ada != -1', 'es inc 406 if fk != -283', 'lx inc 43 if kg <= 7', 'f inc 464 if lx <= 44', 'kg inc 884 if t >= -435', 'mmw inc 836 if gk > -3', 'a dec 496 if um > -1447', 'eri dec -617 if uy == 24', 'j inc -858 if kg < 886', 'hg dec -854 if umr == 789', 'dy dec -246 if f >= 457', 'lbf inc 122 if a != 10', 'aao inc -408 if uy > 19', 'f dec 908 if uy != 18', 't dec -775 if j >= -351', 't inc -594 if yk <= 3', 'es inc 28 if gk == 0', 'es inc -306 if kg >= 894', 'mmw dec 154 if kg <= 885', 'dy inc 832 if aao <= -402', 'lx inc -426 if a >= -8', 'umr dec -792 if eri > -341', 'a inc -609 if gk <= -6', 'j dec -970 if lx > -393', 'uy dec -241 if yk > 0', 'yk inc 411 if is > 61', 'ada dec -253 if is == 66', 'is dec -486 if aao > -413', 'yk dec 561 if a == 0', 'dy inc 976 if um == -1454', 'dy inc 885 if eri < -331', 'hg inc -5 if gk <= -9', 't dec 717 if f <= -443', 'mmw inc -293 if lx <= -379', 't inc 77 if lx != -383', 'uy dec -89 if ada <= 258', 'fk inc -381 if fk < -272', 'eri dec 711 if mmw < 398', 'is dec -273 if gk != -3', 'umr dec 384 if aao != -414', 'is dec -36 if is != 825', 'ada dec 422 if es < -326', 'fk inc 207 if mmw < 389', 'uy dec -357 if lx == -383', 'es inc 829 if dy <= 3199', 'aao dec -173 if gk == 0', 'x dec 274 if is >= 824', 't dec -400 if is <= 833', 'fk dec -677 if f == -444', 'x inc -494 if j == 623', 't dec -406 if f < -443', 'gk dec 704 if gk == 0', 'x inc -637 if x < -758', 'x dec 194 if gk != -710', 'um inc 956 if fk > 26', 'ada inc -527 if aao > -239', 'j inc -774 if f <= -436', 'es inc -121 if ada > -689', 'hg dec -461 if gk < -698', 't inc 780 if is < 828', 'yk inc -858 if es >= 504', 'dy inc 145 if j > -159', 'is inc 929 if f != -453', 'mmw inc 702 if fk > 17', 'lbf dec 123 if aao >= -240', 'hg dec -543 if a == 0', 'kg dec -610 if es > 488', 'hg inc -726 if hg < 1854', 'kg dec -410 if j <= -146', 'dy inc -469 if gk <= -712', 'a inc 252 if aao > -237', 'dy dec 168 if uy <= 478', 'gk inc -530 if a > 244', 'gk dec -254 if uy == 479', 'es inc -960 if j > -152', 'umr dec 561 if hg != 1126', 'uy inc 420 if j < -148', 'mmw inc 976 if j < -142', 'umr dec -852 if gk >= -1238', 'aao dec 559 if eri >= -1042', 'gk inc -745 if j <= -142', 't dec 183 if hg < 1112', 't inc 725 if yk == -150', 'lbf dec -142 if kg < 1912', 'mmw dec -908 if is <= 1758', 'um inc 329 if f == -447', 'x dec 543 if ada > -704', 'gk inc 226 if eri <= -1041', 'es dec -176 if mmw == 2975', 'ada inc -156 if eri >= -1053', 'ada inc -523 if t <= 1347', 'aao inc -717 if x < -2145', 'gk inc -236 if t >= 1354', 'lx dec -266 if lx != -389', 'hg dec -324 if dy >= 3169', 'f dec 96 if x != -2143', 'yk inc -270 if um != -1450', 'aao inc -916 if lbf == 141', 'es inc -943 if f == -540', 'a dec 974 if lbf > 131', 'dy dec -35 if yk == -413', 'kg inc 112 if eri >= -1053', 'mmw inc -30 if gk <= -1754', 'um dec -288 if mmw < 2978', 'es dec 774 if uy == 900', 't dec -60 if x > -2145', 'j inc 1 if x > -2148', 'dy inc 222 if es >= -1232', 'is dec -221 if x != -2142', 'hg dec -626 if uy > 887', 'is dec -114 if t <= 1408', 'j inc -564 if umr == 1488', 'a inc -29 if f != -540', 'umr dec 373 if fk != 17', 'a dec -788 if fk >= 14', 'ada inc 316 if aao >= -1153', 'x dec 970 if lbf != 141', 'x dec -209 if aao >= -1159', 'uy dec 279 if lx != -117', 'f dec 517 if hg >= 2065', 'j dec 566 if a <= 75', 'x dec -346 if a <= 59', 't inc 576 if lx > -118', 'um dec 785 if es >= -1229', 'a dec -949 if mmw > 2974', 'j inc 915 if x <= -1929', 'hg inc 177 if is < 1873', 'is inc -678 if f >= -1052', 'umr dec 254 if lx > -123', 'x dec 754 if um < -1160', 'aao dec 977 if uy <= 894', 'yk inc -157 if aao <= -2124', 'um inc 631 if is >= 1867', 'lx inc -99 if ada <= -1058', 'fk dec -834 if x < -2695', 'is dec 105 if x != -2680', 'a inc 462 if umr <= 864', 'mmw inc 394 if lbf > 150', 'gk inc -370 if lbf >= 146', 'is inc 722 if yk > -586', 'dy inc -882 if gk != -1753', 't inc 983 if gk == -1763', 'fk dec 874 if fk > 14', 'hg dec -949 if lbf < 142', 'es dec -592 if uy == 891', 'dy dec 823 if gk >= -1762', 'mmw dec 137 if gk >= -1751', 'hg dec 704 if dy >= 2343', 't dec -921 if j != -372', 'x dec 95 if is >= 2485', 'dy inc -117 if kg >= 2017', 'gk dec 551 if um <= -545', 'ada inc -161 if umr >= 856', 'mmw inc 633 if umr != 862', 'fk dec 38 if lbf >= 140', 'kg dec -954 if x >= -2787', 'um inc 325 if hg > 2481', 'um dec -72 if j > -375', 'umr dec 910 if gk <= -1756', 'fk dec -628 if j != -356', 'mmw dec 267 if aao != -2123', 'eri inc -857 if um != -137', 'um inc -651 if eri != -1896', 'j dec -122 if a >= 1473', 'umr dec 177 if gk == -1753', 'mmw inc -16 if t > 2911', 'eri dec 502 if um <= -785', 'hg inc 134 if x != -2775', 'lx dec 263 if kg <= 2978', 'hg dec 83 if es != -1235', 'mmw dec -837 if umr <= 693', 'dy inc 148 if um < -792', 'gk inc -13 if j > -247', 'x dec 749 if yk >= -568', 'lbf inc 606 if is != 2489', 'x inc 588 if dy >= 2345', 'dy dec 243 if yk <= -574', 'umr dec 1 if es == -1233', 'f dec 104 if t == 2903', 'aao dec 32 if es != -1224', 'x inc 882 if j < -245', 'hg inc -998 if uy == 890', 'dy dec -605 if dy <= 2115', 'hg inc 45 if gk != -1769', 'lbf inc -521 if t > 2894', 'umr inc -115 if a != 1473', 'lx dec -795 if x == -2194', 't inc 143 if f < -1154', 'es dec 629 if is > 2494', 'lbf inc 195 if fk <= -263', 'fk inc 926 if aao <= -2153', 'um inc 351 if es != -1230', 't dec -541 if lx != 316', 'mmw inc -329 if mmw != 4178', 'dy inc 708 if is > 2481', 'j inc 386 if t != 3050', 'hg dec 253 if umr == 568', 'um inc 236 if mmw >= 4172', 'fk inc -874 if hg != 1328', 'lbf dec -499 if um != -202', 'lbf dec 999 if gk > -1774', 'gk dec 474 if fk > -219', 'mmw dec -598 if yk > -585', 'fk inc -508 if t == 3046', 'mmw inc -638 if x == -2193', 'f dec 756 if a == 1477', 'mmw dec -339 if aao > -2161', 'um inc 109 if lbf <= -578', 'fk dec -421 if lx < 321', 'is inc -725 if ada >= -1226', 'fk dec -458 if ada >= -1226', 'uy dec -588 if aao <= -2160', 'ada inc 404 if dy != 3420', 'x inc 788 if f <= -1910', 'kg dec -520 if is == 1754', 'es dec 895 if lbf < -568', 'fk dec -999 if lbf == -578', 'kg dec -38 if lbf != -574', 'uy inc 343 if lbf != -579', 'is dec -176 if es <= -2125', 'lbf dec -680 if lbf < -573', 'eri inc 562 if uy != 1823', 'x inc 87 if fk >= 1158', 'umr dec -850 if eri > -1843', 'um inc -978 if eri <= -1849', 'x dec 389 if gk < -2241', 'f inc -288 if a != 1486', 'kg dec -484 if uy < 1826', 'lx dec -328 if lbf != 97', 'um inc -998 if gk <= -2240', 'yk inc 314 if mmw <= 5120', 't dec -884 if es == -2128', 'uy dec 190 if f <= -2199', 'lx dec 128 if umr > 1425', 'eri inc 807 if a > 1485', 'ada inc 272 if umr < 1422', 'hg inc 630 if is == 1937', 'um dec 143 if ada >= -949', 'eri dec -334 if lx != 637', 'fk dec 147 if umr < 1426', 'gk dec 309 if uy == 1631', 'aao dec 233 if hg == 1336', 'is dec 825 if yk > -271', 'lbf dec -498 if umr <= 1413', 'kg dec 473 if es > -2131', 'mmw dec -728 if hg != 1327', 'dy dec 309 if hg <= 1341', 'dy inc -863 if kg >= 3023', 'x inc -465 if lx <= 647', 'a inc 253 if x >= -1793', 'kg inc -184 if eri < -1500', 'um inc -527 if lx != 652', 'j inc -455 if hg > 1328', 'eri inc 866 if yk != -263', 'aao inc -47 if gk > -2553', 'gk inc 228 if gk < -2554', 'gk inc -493 if fk <= 1006', 'mmw inc 800 if x == -1784', 'lbf inc -351 if umr < 1426', 'a inc -903 if ada > -958', 'umr inc 942 if es != -2128', 'dy inc 600 if a < 830', 'j dec -247 if lx < 646', 'gk dec -922 if t >= 3930', 'mmw inc -114 if lx != 654', 'fk dec 415 if um > -1764', 't inc -763 if lbf < -246', 'ada inc 818 if is > 1108', 'uy inc -839 if t != 3171', 'fk inc -335 if is > 1106', 'fk dec -335 if yk == -263', 'fk inc -291 if dy == 3711', 'lx dec -665 if yk != -263', 'es dec -772 if uy != 792', 'umr dec -528 if um != -1764', 't dec -95 if es < -2137', 'es inc -800 if yk >= -261', 'kg inc 150 if j >= -70', 'f dec -118 if mmw < 6536', 'a inc 595 if uy > 794', 'is inc 927 if lx > 636', 'eri dec -61 if x != -1785', 'hg inc -878 if yk != -260', 'gk inc -727 if fk <= 305', 'mmw dec -945 if a <= 833', 'aao inc -101 if x >= -1792', 'hg dec 567 if es > -2131', 'gk inc -689 if mmw < 7484', 'ada inc -644 if eri > -1452', 'yk inc -810 if yk > -265', 'um dec 655 if aao < -2533', 't dec 179 if umr != 1943', 'gk inc 833 if hg >= -110', 'fk dec 998 if fk < 315', 'a dec -558 if aao > -2543', 'x inc 426 if lbf == -249', 'uy inc 892 if yk > -1075', 'umr inc 250 if es <= -2127', 'mmw inc -727 if umr >= 2193', 'kg dec 111 if es == -2128', 'dy dec 898 if fk != -693', 'yk dec 168 if umr >= 2191', 'uy dec 113 if dy <= 3711', 'mmw inc -752 if yk == -1241', 'yk inc -181 if t > 2989', 'mmw dec -636 if t < 2995', 'a inc -424 if hg == -109', 'j dec -762 if ada > -780', 'lx dec 565 if uy <= 1577', 'aao dec 858 if j == 697', 'fk inc -383 if a < 969', 'eri inc -51 if lx <= 85', 'aao inc 666 if j > 690', 't dec 234 if a == 964', 'aao inc -69 if fk > -1085', 'es inc -721 if gk >= -2215', 'is inc -185 if lbf > -251', 'mmw dec 411 if es == -2849', 'f dec -214 if gk == -2210', 'yk inc 904 if aao >= -2804', 'es inc 883 if mmw != 6210', 'x dec 6 if ada != -774', 'aao inc -776 if um != -2419', 'j inc -653 if yk == -344', 'gk dec 338 if fk != -1072', 'yk inc -13 if x >= -1360', 'lbf inc 201 if dy < 3716', 'yk dec -904 if aao != -3575', 'f dec 922 if j == 697', 'uy dec -562 if lbf != -53', 'gk dec 50 if lbf <= -47', 't inc -670 if mmw > 6222', 'lx inc 515 if uy == 2133', 'yk inc 261 if dy > 3704', 'x dec -854 if uy == 2133', 'kg inc 66 if umr == 2196', 'kg dec -83 if j != 706', 'ada inc 739 if gk > -2590', 'eri dec 379 if eri == -1497', 'dy inc 638 if aao >= -3583', 'a dec 130 if is > 1851', 'mmw dec 399 if uy == 2133', 'eri inc -195 if f > -2801', 'j dec 885 if dy > 4339', 'eri inc -544 if aao == -3587', 'kg inc 895 if t != 2984', 'yk inc 258 if dy <= 4350', 'es dec 660 if dy == 4342', 'umr inc -92 if gk < -2592', 'eri inc 361 if x == -504', 'um dec -298 if gk != -2588', 'fk dec 532 if j < -184', 'uy inc 31 if f < -2791', 'aao dec 31 if j != -182', 'ada inc 448 if um <= -2113', 'fk inc -13 if eri <= -1703', 't inc -59 if es >= -1971', 'gk dec -909 if x == -510', 'es inc 805 if hg >= -112', 'j dec 734 if kg >= 3919', 'um inc 369 if aao != -3606', 'yk inc -548 if dy > 4348', 'gk inc 934 if j < -182', 'x dec 346 if hg <= -107', 'lbf dec -379 if eri != -1718', 'lbf inc -921 if f >= -2802', 'mmw inc -191 if eri <= -1703', 'umr inc 252 if lx != 600', 'mmw dec 410 if ada >= -330', 'gk inc 558 if a != 828', 'mmw dec 320 if um <= -1744', 'ada dec 517 if t < 2933', 'is dec -616 if ada > -835', 'yk dec -406 if j <= -185', 'yk inc -526 if lbf <= -586', 'ada inc 368 if j == -188', 'kg inc -89 if f <= -2791', 'kg dec -531 if lbf == -590', 'mmw inc -252 if f < -2787', 'is inc 293 if eri > -1713', 'lbf inc 509 if kg <= 4367', 'eri inc 607 if fk > -1620', 'f dec -313 if j > -194', 'ada inc -582 if aao >= -3611', 'a inc 373 if x == -850', 'eri dec 668 if ada != -1057', 'um dec 112 if lbf <= -72', 'lx inc 91 if t > 2919', 'a inc 157 if is > 2139', 'fk inc -207 if a != 1371', 'um inc 108 if t <= 2929', 'aao inc 80 if lx >= 681', 'fk inc 437 if lbf == -81', 'umr inc 473 if lbf <= -75', 'eri inc 509 if umr != 2822', 'a dec -7 if is >= 2146', 'fk inc -10 if t != 2920', 'is dec 235 if a > 1358', 'ada inc -655 if eri == -1201', 'kg dec 983 if f >= -2486', 'es dec 640 if t <= 2938', 'eri dec -700 if is < 1919', 'ada inc -213 if fk == -1401', 'hg dec -846 if kg != 3381', 'f dec 584 if a <= 1361', 'aao inc 731 if gk != -1107', 't inc 823 if kg == 3377', 'es dec 382 if j > -195', 'fk inc -83 if ada < -1916', 'umr inc 948 if eri > -511', 'a inc -765 if eri == -501', 'a inc 114 if f > -2478', 'aao inc 343 if aao == -2798', 't inc -172 if eri < -498', 'fk inc 905 if x < -840', 'dy dec -731 if a > 597', 'lx inc 410 if um <= -1744', 'eri inc -859 if lbf <= -90', 'fk dec 820 if ada < -1916', 'yk dec 14 if dy != 5078', 'aao inc -89 if lbf != -81', 'umr dec 242 if aao > -2457', 'f inc -563 if lx <= 1100', 'uy dec 967 if uy <= 2166', 'eri dec 984 if lx > 1086', 'hg dec 816 if mmw <= 4653', 'hg dec -413 if um == -1753', 'dy dec -410 if mmw > 4643', 'uy dec -298 if lx >= 1094', 'mmw dec -611 if dy > 5483', 't dec 471 if is != 1915', 'fk inc 505 if aao >= -2463', 'gk dec -947 if fk == -894', 'es inc -556 if umr >= 3532', 'es inc 768 if x >= -853', 'yk dec -865 if aao == -2455', 'hg inc -481 if a != 609', 'ada inc 904 if es == -1971', 'hg dec -518 if um < -1750', 'yk dec -744 if fk != -889', 'a inc 410 if f > -3047', 'dy inc 522 if is >= 1913', 'um inc 882 if is < 1915', 'es inc -950 if fk > -889', 'is dec -211 if is == 1911', 'kg inc -160 if um == -871', 'a inc 315 if j == -188', 'umr inc 840 if eri <= -1479', 'kg inc -805 if ada <= -1013', 'um inc 701 if x == -850', 'a inc 735 if umr == 4375', 'um inc -413 if lbf != -76', 'dy inc 310 if mmw <= 5268', 'lbf inc -210 if dy != 5800', 'um dec -489 if lx == 1095', 'fk dec -743 if mmw <= 5258', 'lx inc 332 if mmw > 5249', 'hg dec 396 if mmw >= 5251', 'yk inc -672 if fk > -896', 'a inc -872 if t >= 3114', 'a inc 22 if umr >= 4370', 'es inc 374 if um > -98', 'uy inc 609 if lx <= 1434', 'a dec 580 if is >= 2118', 'hg dec -809 if lx >= 1424', 'fk dec 451 if aao != -2446', 'mmw dec -339 if gk < -156', 'hg inc 566 if gk < -153', 'hg inc -629 if uy >= 2100', 'lx dec 314 if a > 1503', 'lbf dec 173 if lx >= 1109', 't dec 107 if ada == -1021', 'dy inc 421 if mmw <= 5607', 'is dec 751 if hg != 731', 'hg inc 844 if hg != 730', 'eri inc -44 if a == 1505', 'uy dec 230 if t <= 3002', 'uy inc -450 if eri < -1521', 'kg dec 353 if j == -188', 'lbf inc -100 if mmw >= 5592', 'umr dec -946 if f >= -3045', 't inc 893 if j == -188', 'lbf dec -263 if hg <= 1572', 'j inc 22 if umr == 5313', 'eri dec 598 if aao >= -2463', 'umr dec -591 if eri > -2130', 't dec 489 if dy <= 6230', 'ada dec -547 if a != 1505', 'eri dec -38 if dy > 6220', 'ada inc 895 if is == 1371', 'is inc -303 if mmw < 5599', 'uy dec -217 if a <= 1513', 'a dec -366 if x <= -851', 'um dec 570 if t < 3411', 'uy inc -560 if mmw <= 5599', 'um dec -234 if gk != -152', 'fk dec 305 if um == -430', 'lx dec -553 if a > 1505', 'yk dec -923 if yk < 1335', 'yk dec 137 if es < -1590', 'hg dec 737 if es > -1605', 'yk dec 607 if eri < -2080', 'um dec -588 if eri != -2097', 'aao inc -230 if aao != -2455', 'fk inc -654 if t >= 3398', 'umr dec 525 if kg != 2064', 'mmw inc -242 if lbf < -90', 'lbf dec 682 if aao >= -2462', 'yk inc -971 if t >= 3402', 't dec -403 if fk <= -2296', 'ada dec 404 if kg == 2059', 'dy inc 95 if yk < 542', 'lbf inc 427 if j <= -182', 'j inc 10 if j <= -179', 'x dec 524 if f <= -3051', 'lx dec 326 if gk != -163', 'umr dec 176 if lx >= 789', 'um dec 264 if eri == -2089', 't inc 197 if eri == -2084', 'dy dec 574 if es > -1605', 'lx inc -898 if um >= -110', 'es dec -845 if um >= -113', 'es inc -731 if yk < 537', 'lx dec 424 if f >= -3053', 'a inc 525 if lx != -535', 'uy dec 692 if yk > 531', 'a inc -591 if fk >= -2309', 'fk dec -204 if aao != -2459', 'mmw dec -420 if fk <= -2110', 'yk inc 166 if j < -168', 'umr inc 535 if gk < -158', 'eri dec 417 if yk >= 695', 'umr inc 230 if mmw != 5363', 'umr inc -36 if lbf < -348', 'f dec -763 if aao < -2450', 'uy inc -841 if es >= -1490', 'is dec -381 if gk >= -167', 'x dec 981 if hg == 828', 'f inc 682 if ada == -530', 'fk inc 268 if uy != -450', 'dy dec 891 if ada < -529', 'uy dec 943 if hg != 828', 'ada dec -496 if a < 907', 'is dec 380 if gk == -159', 'aao dec 772 if eri < -2505', 'umr dec -646 if umr > 6151', 'dy dec 978 if t == 3809', 'kg inc -768 if fk > -1834', 'lbf dec -107 if x <= -1828', 'lx dec 822 if yk <= 709', 'umr inc -504 if ada > -533', 'aao dec -710 if es == -1483', 'uy inc 17 if hg >= 838', 'fk dec -48 if a == 914', 'fk inc -80 if j >= -182', 'gk inc 339 if um < -113', 'lbf inc 224 if f != -1603', 'lbf inc 553 if kg == 1291', 'umr dec -384 if ada > -535', 'lx dec -618 if t == 3809', 'aao dec -291 if ada >= -534', 'lx dec -385 if f <= -1591', 'lbf inc -918 if is <= 1069', 'kg inc 807 if dy != 3871', 'a dec -120 if eri >= -2509', 'fk dec 886 if uy == -452', 'is inc 668 if f == -1600', 'ada dec 281 if dy >= 3872', 'aao inc 952 if j > -182', 'eri inc -279 if kg >= 2098', 'gk inc -357 if gk <= -153', 'lbf inc -255 if um == -106', 'es inc -509 if um < -105', 'j dec 929 if umr < 6681', 'is inc 906 if um != -114', 'ada dec 951 if gk >= -523', 'aao dec 80 if kg > 2089', 't inc 811 if hg < 832', 'yk inc 303 if f > -1601', 'gk inc 180 if mmw <= 5351', 'is dec -639 if umr < 6672', 'mmw dec -142 if kg <= 2103', 'fk dec -275 if is != 2643', 'ada inc 568 if x <= -1822', 'a dec 677 if yk != 1005', 'yk inc 111 if es <= -1990', 'eri inc -17 if eri >= -2793', 'lbf inc 974 if gk == -516', 'hg inc -723 if lbf == 337', 'mmw dec 408 if dy <= 3877', 't dec 142 if mmw < 5084', 'gk dec 53 if yk != 1111', 'lbf dec -434 if aao != -1344', 'kg dec -837 if f >= -1593', 'f inc 513 if eri <= -2804', 'fk dec -925 if fk >= -2756', 't inc 280 if kg != 2100', 'lx dec 328 if dy < 3880', 't inc -359 if j < -1103', 'es inc 289 if ada < -1203', 'x dec -414 if gk >= -574', 'aao dec 710 if dy == 3873', 'es dec -70 if ada <= -1187', 'ada dec 883 if j == -1110', 'is dec -635 if um != -105', 'is inc 627 if a == 1034', 'um inc -348 if ada > -1190', 'mmw dec -270 if uy >= -454', 'ada dec 362 if is > 3900', 'eri dec -504 if t != 4541', 'uy inc 910 if eri >= -2804', 'es dec 261 if fk < -1821', 'uy dec -430 if uy >= 456', 'yk dec -841 if um >= -107', 'j dec -287 if fk >= -1834', 'a dec 90 if uy <= 897', 'lx inc 867 if hg < 819', 'yk dec 265 if fk >= -1820', 'is inc -444 if umr >= 6676', 'kg inc 586 if f == -1600', 'es dec -298 if uy != 889', 'mmw inc -896 if gk >= -576', 'a dec -320 if t >= 4538', 't dec -722 if hg >= 819', 'mmw inc -778 if ada < -1553', 'um dec -914 if j != -826', 'kg inc -964 if f < -1605', 'yk inc -51 if umr >= 6670', 'um dec 219 if j == -820', 'dy inc 727 if a == 1264', 'a dec -817 if kg <= 2692', 'um dec 99 if fk == -1826', 'kg dec 302 if uy != 892', 'j dec -696 if lx <= -688', 'uy inc -626 if t <= 5268', 'a dec 961 if hg <= 837', 'yk inc -803 if a != 1119', 'mmw dec 678 if lx < -680', 'lbf inc 862 if fk < -1825', 'kg inc -786 if t <= 5259', 'aao dec 91 if x == -1407', 'uy dec -548 if t == 5263', 'aao inc 638 if is != 3463', 'hg dec 244 if uy > 807', 'f inc 58 if lbf >= 765', 'fk inc 581 if is != 3455', 'hg dec -692 if fk >= -1247', 'um inc -752 if aao < -1424', 'lbf dec 14 if lbf != 783', 't dec 270 if f == -1542', 'uy inc 70 if hg <= 1277', 'is inc 676 if lx == -682', 'is inc 230 if um >= -163', 'gk dec 799 if yk > 1107', 'ada dec -20 if eri != -2804', 'lx dec -278 if umr == 6678', 'gk inc 83 if umr <= 6686', 'lbf inc 265 if a >= 1118', 'is dec 476 if j != -820', 'eri dec 509 if lx > -413', 'is dec -486 if dy < 4606', 'kg dec 989 if is > 4847', 'lx inc 996 if dy >= 4591', 'is inc -371 if eri > -3303', 'kg dec 209 if f != -1542', 'kg dec -21 if kg < 1394', 'uy dec -34 if x == -1417', 'mmw inc -753 if hg != 1285', 'gk dec 862 if kg > 1408', 'ada dec 346 if is < 4856', 'umr inc 262 if es > -1888', 'lx inc -842 if umr < 6948', 'f inc 557 if yk != 1103', 'dy inc -323 if lbf >= 1030', 'kg dec 610 if ada >= -1883', 'f dec 727 if f != -1544', 'es dec -922 if aao > -1435', 'kg inc -628 if f == -2269', 'eri inc -762 if lx < -245', 'a dec 246 if a <= 1118', 'aao dec 51 if kg >= 181', 'is dec 761 if x >= -1417', 'j inc 359 if x == -1417', 'mmw dec 562 if ada < -1880', 'lbf dec 955 if aao != -1426', 'umr dec -851 if x == -1417', 't dec -845 if is <= 4101', 'lbf inc -666 if hg > 1272', 'um dec -105 if f >= -2274', 'gk inc 191 if umr != 7781', 'dy dec -399 if eri <= -4072', 'is inc 681 if t != 5835', 'mmw inc -731 if ada > -1883', 'x inc -603 if yk < 1111', 'j inc 860 if fk <= -1239', 't dec -480 if kg > 175', 'eri inc 308 if mmw > 957', 'hg inc 37 if gk >= -1163', 'eri inc 868 if kg >= 172', 'gk inc 381 if f > -2276', 'ada inc -231 if fk < -1234', 'uy dec -404 if gk >= -781', 'es inc -33 if yk != 1105', 'j inc -210 if um != -66', 'umr dec -783 if kg == 176', 'a inc 287 if hg < 1322', 'es inc 794 if f >= -2270', 'f inc 816 if a < 1417', 'eri inc -136 if fk <= -1235', 'j dec 421 if lbf < 362', 'kg dec -889 if fk > -1248', 'um inc 701 if yk <= 1110', 'x dec -487 if fk < -1243', 'aao dec 623 if umr <= 8582', 'mmw dec -307 if eri > -3038', 't inc 803 if f == -1453', 'kg dec 980 if a < 1404', 'dy inc -974 if gk < -772', 'yk inc 221 if eri < -3040', 'gk inc -421 if aao > -2059', 'mmw dec -751 if f <= -1445', 'kg dec 422 if lx <= -250', 'dy dec 191 if x <= -1535', 'um inc -318 if gk != -1195', 'mmw inc 870 if kg != 651', 'j dec -865 if t < 7131', 'um dec 886 if t < 7124', 'ada inc 171 if eri < -3030', 'x dec -755 if es == -202', 'fk inc -325 if hg >= 1313', 't dec 984 if t != 7130', 'j dec 55 if aao == -2056', 'fk dec 80 if x <= -773', 'dy dec 852 if lx != -256', 'is inc 295 if a >= 1408', 'uy dec 733 if hg < 1318', 'x inc 868 if um <= -560', 't dec -532 if t != 6128', 'aao inc -530 if x == 90', 'is dec 374 if lbf == 358', 'aao inc 93 if t == 6673', 'uy inc -657 if hg != 1317', 'fk inc -670 if umr > 8568', 'x inc 791 if j != 634', 'mmw dec -872 if uy >= -73', 'yk inc -771 if eri <= -3034', 'umr dec -125 if kg < 645', 'mmw inc -617 if aao > -2581', 'mmw dec -90 if mmw != 3145', 'es dec 182 if aao <= -2574', 'kg dec 903 if ada >= -1934', 'um inc 319 if lbf == 358', 'uy inc -958 if f <= -1447', 'ada dec -965 if eri == -3033', 'fk dec 750 if es >= -393', 'hg inc -488 if hg >= 1307', 'lx inc 742 if umr != 8703', 'uy inc 378 if kg != 643', 'lx dec -584 if um != -233', 'kg dec -654 if ada >= -986', 'is dec 181 if f == -1453', 'eri inc 302 if lx < 1080', 'uy inc -907 if kg != 1289', 'yk dec 652 if is < 4223', 'lbf inc -147 if hg != 823', 'fk dec -584 if kg < 1300', 'fk dec -593 if f <= -1449', 'dy dec -83 if gk < -1189', 'a dec -568 if es <= -377', 'aao inc -742 if gk <= -1193', 'kg dec -560 if hg <= 831', 'es dec -871 if fk > -1899', 'lx inc 239 if kg != 1855', 'uy dec 696 if ada >= -984', 'kg dec -899 if yk >= 452', 'x inc -303 if is <= 4223', 'um inc -207 if lbf != 211', 'eri dec 520 if eri >= -2731', 'is dec -251 if t < 6675', 'umr inc 19 if kg == 1857', 'lbf dec -365 if uy != -2632', 'yk dec 192 if fk < -1883', 'dy dec 451 if hg > 820', 'j dec -789 if lx <= 1320', 'um dec -577 if lx > 1309', 'es dec 954 if dy != 2800', 'aao dec 798 if f <= -1446', 'mmw dec -339 if mmw >= 3143', 'j inc 126 if yk == 259', 'ada inc -898 if umr != 8718', 'kg inc -365 if eri == -3251', 'aao dec 718 if lx > 1307', 'x inc -872 if kg <= 1495', 'j dec -862 if is != 4464', 'mmw dec -785 if is == 4469', 't dec 355 if uy != -2627', 'ada dec -528 if ada == -977', 'yk dec -139 if hg >= 823', 'mmw dec -97 if is == 4469', 'j dec -454 if is == 4469', 'yk dec -151 if kg < 1500', 'lbf inc -19 if lbf != 576', 'yk inc 281 if umr == 8718', 'gk dec 59 if mmw <= 4374', 'umr dec 266 if hg < 828', 'fk inc -54 if is <= 4477', 'is inc 468 if is >= 4477', 'mmw inc -749 if ada != -442', 'is inc 22 if mmw > 3608', 'uy inc -436 if ada != -449', 'umr dec -545 if gk == -1256', 'mmw inc -716 if ada <= -447', 'fk dec -470 if f >= -1450', 'ada inc -429 if uy != -2633', 'aao inc -28 if a < 1984', 'umr inc -826 if aao >= -4867', 'lbf dec 141 if kg < 1493', 'lbf inc 307 if eri == -3251', 'um dec -120 if um == 335', 'j inc -674 if fk == -1956', 'mmw inc -784 if lx == 1315', 'x inc -524 if dy == 2805', 'mmw dec 911 if kg == 1492', 'gk inc 260 if mmw >= 1200', 'es inc 638 if hg > 819', 'mmw dec 276 if ada == -449', 'eri dec -682 if kg != 1489', 'um inc 790 if t > 6321', 'a inc 288 if eri >= -2560', 'eri dec -477 if lbf >= 747', 'kg inc 922 if kg > 1489', 'ada dec -65 if uy >= -2634', 'ada dec -106 if umr >= 8170', 'is dec -609 if aao >= -4866', 't dec -598 if mmw == 930', 'gk dec 89 if t != 6912', 't dec -500 if f < -1456', 'is dec -169 if es == 171', 'f dec -633 if f <= -1453', 'aao dec -191 if t > 6905', 'a dec -772 if eri > -2574', 'x inc -272 if x >= -818', 'es dec 135 if j <= 2862', 'uy inc 950 if aao == -4674', 'ada dec 380 if aao != -4676', 'aao inc 111 if kg < 2415', 'lx inc -339 if umr == 8171', 'yk dec 63 if ada <= -653', 'yk inc -894 if j > 2863', 'f dec -590 if eri != -2560', 'hg inc -281 if gk == -996', 'lx inc -529 if hg >= 539', 'ada dec -133 if es != 163', 'f dec -510 if t != 6912', 'uy inc -761 if um != 465', 'a inc -466 if um > 452', 'f dec 811 if lbf <= 747', 'umr dec 206 if umr >= 8170', 'x dec -606 if dy <= 2814', 't dec 823 if hg <= 553', 'yk inc 130 if um != 453', 'aao inc 984 if fk > -1948', 'x dec -152 if um > 447', 'fk dec -958 if kg > 2418', 'eri dec 996 if a < 2290', 'aao inc 702 if x != -330', 'lbf dec -8 if aao > -2872', 'mmw inc 346 if hg != 554', 'is dec -255 if fk == -1946', 'gk dec -139 if x >= -335', 'j dec -238 if x != -332', 'lbf inc 649 if a < 2283', 'lx inc 702 if es < 178', 'fk dec -918 if j > 2858', 'lbf inc 971 if hg == 544', 'f dec -807 if a < 2283', 'eri dec -263 if dy != 2814', 'fk dec 128 if kg == 2414', 'hg dec 541 if mmw > 1270', 'uy inc -144 if um <= 458', 'um dec 362 if mmw == 1276', 'yk inc -346 if mmw == 1276', 'mmw inc -543 if yk <= -340', 'hg inc -358 if mmw == 733', 'es dec -652 if f >= -232', 'uy dec 401 if ada == -525', 'x inc 736 if kg >= 2412', 'uy inc -489 if mmw == 733', 'yk inc 134 if is > 5522', 'lbf dec 531 if uy != -3470', 'f inc 472 if umr >= 7960', 'f dec -410 if lbf >= 1836', 'eri inc 522 if gk == -857', 'um inc -672 if es != 178', 'fk dec -774 if j <= 2871', 'f inc 825 if kg != 2414', 'j dec -713 if es <= 178', 'um inc 769 if t <= 6079', 'lx inc 995 if dy > 2797', 'is dec 359 if es < 180', 'a inc -680 if es < 177', 'eri inc -102 if mmw < 736', 'ada inc 39 if eri != -2889', 'lx dec -935 if lx != 2145', 'hg inc 741 if es >= 165', 'kg dec -156 if lbf <= 1835', 'f dec 376 if eri > -2892', 'aao inc 570 if j == 3577', 'dy inc 708 if is > 5162', 'a dec 737 if aao == -2307', 'x inc 936 if hg == 391', 'aao inc -405 if j > 3576', 'mmw inc -42 if kg > 2561', 'j dec 295 if um != -588', 'yk dec -641 if j <= 3282', 'umr inc -633 if gk != -864', 'dy inc -202 if gk < -858', 'aao inc -244 if gk != -861', 'uy inc -97 if kg == 2573', 'mmw dec -889 if ada < -482', 'es inc -166 if fk == -382', 'eri dec -962 if eri >= -2889', 'umr dec 201 if t >= 6086', 'gk dec -700 if mmw == 1580', 'ada inc -158 if gk < -159', 't inc 650 if es < -2', 'lbf dec 870 if aao > -2966', 'uy dec 727 if j <= 3289', 'umr inc 483 if lbf < 971', 'hg dec -283 if fk != -379', 'kg dec 202 if t < 6090', 'eri inc 607 if a >= 864', 'lbf dec 282 if lx > 3074', 'yk dec 490 if mmw >= 1573', 'uy dec -536 if aao >= -2959', 'uy dec -306 if lx > 3071', 'fk dec 982 if lx == 3069', 'aao dec 431 if aao < -2947', 'mmw inc 145 if t < 6093', 'is inc -222 if es <= 11', 'mmw inc -953 if fk < -372', 'a inc 588 if x != 406', 'gk dec 464 if lx <= 3080', 'mmw dec -655 if a > 1448', 'mmw dec 251 if aao < -3394', 't inc 582 if dy < 3508', 'lbf dec 816 if ada < -492', 'uy inc 374 if a >= 1445', 'f inc 98 if f >= -129', 'gk dec -206 if gk == -621', 'lbf dec -368 if fk != -382', 'mmw dec -16 if um == -579', 'dy dec 522 if umr == 7614', 'fk inc -645 if dy != 2998', 'hg dec 829 if lbf > 676', 'aao dec 472 if t != 6098', 'kg inc 926 if aao >= -3868', 'x dec -485 if j <= 3284', 'x dec 987 if mmw > 1433', 'yk dec -933 if aao != -3859', 'fk inc -446 if lx <= 3080', 'kg dec 573 if f != -129', 'hg dec 231 if dy <= 2992', 'eri dec -162 if es < 14', 't dec 975 if lx > 3086', 'dy dec -144 if f < -147', 'lx dec 122 if lbf < 682', 'mmw inc -438 if umr == 7614', 'j inc 149 if mmw < 1009', 't inc 749 if lx > 2947', 'um inc -970 if hg >= -400', 'kg inc 368 if kg != 2721', 'aao dec 845 if kg == 2721', 'eri dec -521 if yk > -59', 'gk dec -200 if ada >= -495', 'hg inc 462 if um == -1549', 'eri dec -54 if mmw >= 998', 'hg dec -268 if a >= 1450', 'j dec 86 if t != 6840', 'a dec -394 if a == 1452', 'aao inc 166 if kg >= 2720', 'x inc -146 if is == 4943', 'es inc 496 if kg < 2723', 't dec -949 if uy <= -2989']
from collections import defaultdict
import re
finder = re.compile(r'(?P<register>.*) (?P<operation>inc|dec) (?P<value>-?\d*) if (?P<check1>.*)(?P<check2> [!=><]{1,2} -?\d+)')
def solve(data):
    registers = defaultdict(int)
    for line in data:
#         print(line)
        m = finder.match(line)
        if not m:
            raise Exception(line)
        d = m.groupdict()
#         print('{}({}){} == {}'.format(d['check1'], registers[d['check1']], d['check2'], eval('{} {}'.format(registers[d['check1']], d['check2']))))
        if eval('{} {}'.format(registers[d['check1']], d['check2'])):
            if d['operation'] == 'inc':
#                 print('{}({}) += {}'.format(d['register'], registers[d['register']], d['value']))
                registers[d['register']] += int(d['value'])
            else:
#                 print('{}({}) -= {}'.format(d['register'], registers[d['register']], d['value']))
                registers[d['register']] -= int(d['value'])
    
    print(max(registers.values()))
    return max(registers.values())
    
test_data = """b inc 5 if a > 1
a inc 1 if b < 5
c dec -10 if a >= 1
c inc -20 if c == 10""".split('\n')
assert solve(test_data) == 1
print(solve(data))
finder = re.compile(r'(?P<register>.*) (?P<operation>inc|dec) (?P<value>-?\d*) if (?P<check1>.*)(?P<check2> [!=><]{1,2} -?\d+)')
def solve(data):
    highest = 0
    registers = defaultdict(int)
    for line in data:
#         print(line)
        m = finder.match(line)
        if not m:
            raise Exception(line)
        d = m.groupdict()
#         print('{}({}){} == {}'.format(d['check1'], registers[d['check1']], d['check2'], eval('{} {}'.format(registers[d['check1']], d['check2']))))
        if eval('{} {}'.format(registers[d['check1']], d['check2'])):
            if d['operation'] == 'inc':
#                 print('{}({}) += {}'.format(d['register'], registers[d['register']], d['value']))
                registers[d['register']] += int(d['value'])
            else:
#                 print('{}({}) -= {}'.format(d['register'], registers[d['register']], d['value']))
                registers[d['register']] -= int(d['value'])
        highest = max(highest, registers[d['register']])
    
    print(highest)
    return highest
    
test_data = """b inc 5 if a > 1
a inc 1 if b < 5
c dec -10 if a >= 1
c inc -20 if c == 10""".split('\n')
assert solve(test_data) == 10
print(solve(data))
data = """{{{{{{{<!!"!!!>},<>},{<o!>},<u!!i!!'!>,<!!!>,e{'e!!!>},<!i>}},{{<"o!!"!>,<>},<!io<>},{{},<!!!>!>,<o"e!<!!!>{,!!!>{a!o,au!>},<>}}},{{{<e!}>},{{<!>,,e!!!>!!,>},{<a!!!>'!!!>!!!!,!!!>!!!>!>},<<{"!!>}},{{<!>>,<!>},<i!>!<>},{<!!<u,a"!>},<o{{!!{!!!>i,!>,<i{!u>,{<a!>e}o!>!>e>}}}},{{<i<!>,<!!!>,<ei,!>a>,{}},{<!!!>},<e'>,{}},{{<!!!!u<,'}!>,<"o<>}}}},{{{{{{<!>,<o!!!auii!!!!!>!!!>,<{>}},<},!!!>!!!!!>>},{<'u<"{>,{<!!!!e!>,<'a!!i<!>,>}},{}},{{<i}<!u<{!!!}!!e!{!,>}},{<!!e,!>i>,{}}},{{<i!!!>},<{''i!!!>,!e!>},<!>"a{>,<!!'u!!!>},<>}},{{{},<i!>},<<!>},<">},{{<!>,<o!!!!e{uee!!}o<ei{i!>,<!!!>,<>},<,!>},<a!>>},{{},{<}i,!'!!<!!!>}>}}}},{{{{{},{},{{<i!>,<!"!!!>!!!>''>,{}},{{<!>},<u!a!!!>!u!"'!!{!!!>!!!>!!i!!!>,<,a!!!>i!>},<">,{}},{<!!!eoo!!!!ai'!!u!!!>!o>,{<,!!!>aai}{}}"'>}},{{},<i'ia,!!!>o!>,<"!!u!>>}},{<!!!>{u!!!>,<,<!>},<'<}<'"!>},<!u>}}},{{{{<}!!a}!>},<'>},{}},{{{{{},{{<i{!'u}}{>,{{{{<}!>,<!!!!uau!{''!!}ua>}}},{}}},{{{<!!},!!""!!!>,<i!'!{!>},<o>},{<a!u!!"<!>},<"!,{<<e!!<!!u!>},<!o!!{}>}}}}},<,o}!>,<!!!!'!'a!!{>}},{{{<<>},{{<ui{!!i!>{'!!!>},<'>}}},{<{!!!>},<!a!e!!!>o'i!!<'!>,<o!!e!!"!>,<!>>},{<{a>}}}},{{{{<"{!!!>,e!!!>"a!!}!!!,!>>},<o!!!>>},{{<o!{}!!!>},<!!,!!",!>!!!>!>,<ee!>,<!>!u>,<!oo"u}!!ua!>},<!>},<iie>}},{{<!!!>>},<!!e{!!!!!!!>},<}!!{}!!}<,>}}},{}},{{{<!>!>},<e",!>,<!>,<!>{!!<!>oi>},{<!>!!!>{}o!!!>!>}a!!>}}}},{{{{},{<"!!u">}},{{{<"e!>,<u{<}>},{}},{<!!!>,!!!>!>,<,!}!!!!'ei!!i,>,{<!!a"ua!!!>>}}},{}},{{<!!a!!!>!!}eu!!}{{a"">}},{{<u!>,<!>},<!!!>oi!!!>!>!>},<'e{u!'}!>,<!>},<!e>,{<u!!!>}!u<!a>}},{{{<!><!>},<!!!>ii,>}}},{<!>u{'!!!>{i!o}}e!!!>},<a!!!>,<>}},{}}},{{{{{{<ao!!>},{}}},{{<"!!<!>},<>},{<>}}},{<{>},{{<!!!>e!>},<u!!,!!ou}i'e"i>},{{{{}}},{<o!!'!o!!!!!>!ao{<!>>}}}}},{{{{<}}!!!>o!><}o!!{!!!>i!!,>},{{<!!!>'!!!><!>,<>}}},{{{{<o!>!>},<,!!!>o{i{>},{{{{<!>},<a!uo",!>,<!>},<e!>{,}!>},<!>,<>}},{}},{}}}},{{<a!>},<"i!!!!!>,<!!!>"!!oa!!!>!!{!!!!!>!a>,<<{!!!>,<!>"}!>},<!>,<!"!!!"!!ou!>{u!!!>>},{{<<!>,<!!'!!'o"!!!!o"}!i>}},{<}!!}!!}<{>,<!!!>,u!>},<o!ae'u!>},<!>},<<u!e>}}},{{{{<!>eui",o!!!>!>"i>,{<!!!,!!u!!>}},{{<!<>}},{<'!>,<ia!!!!!>},<ea!!!o!>!!!>!<'!e!>},<>,<>}},{{{{<a!!!>!!!>,<'o>}}}}},{{{<!!!>},<,a'a'!!!>,iu"'!>,<}>,{}},{{<!>!>,<<!!!!!>>,<!!!>!>>},{{<,!>,<oe!"!>!!u!',ia'"!>,<!>,<,>},<<!!!!'!!!}}!!!e!!!>,!>},<}!!!!!>,<>},{<"ia!!a!!!!}i!>'>,<"aio!>,<"e"e{!!i!!!>o!{!>!!!!"">}},{{{{{<",u!!{!!{!!<!>},<!u!!,!!!!!>!!!!!!!><"!>},<>},{{<'!"o,!>},<!>,<",!!!!uu!!i!!!>!!"!!!>,<>}}},{{<'!!!!a<<!!!!{u!!,!>},<!>},<o!>},<ouu!!!!!"!!!>>,<!!!>}'{!!a!!"!>},<,ao!!!!!!!>!>!!,<!!!>}>},{},{{{<'!!{"}iu!!e!>!>uo!!}!>,<,!>a>},<<!!!>,!ae!>!>,<a<!!,>}}}},{{{<u!<>},{}},{{{{{{}},<!!!>a!>},<{>}},{<!!<<!>!!!>i!!!>!>},<}{,!!a>,<!>!>"<,e!ee!>,<}!>}"!!!>!!!>o>},{{{},{{},{{{},{<<<'!!!>!>u'i,{!!!>!<!!!>a!>,<>}},<!>!!!><!!!!i!!!>}!,"!!!>!!!>>}}}}},{}}},{{<<eo!!!>!!!!!!!>{{!!!>iou,a'!>,<,>},{}}},{{{}}},{<{!!!>!>,<!!!>},<!!!!}!!!!,a!""}ie!"a>}}},{<!!!!!>!!'',eu!e!>!!!>!>},<>,{{<e''u!>!>,<a!ui}u!>,<>}}},{{<'>}}},{},{{},{{}},{}}},{}},{{{{{<!!""!!,a<>}},{<',<!!!><!!!!},"}>}},{{{{<>}}}}}}},{{{<}>,<<u{!>},<!!"i!aeu!>o"o}o>}}},{{{{{<u!!ee,e>},{<u!!!>!>,<!>},<o>}},{},{<!>o{!!!!i{!>},<o!>"!!u}<e"}!!i">,<i!!!"e!>,<!>,<>}},{{{{<u!>},<!!!>'!!!>!!!!!>}{!>}a!>,<u'!>{!!!>'>,<o"!>,<u>},{<!!uoa>,{{<!!!>,<u}>}}}},{{{{<!>},<!!!><u<>}}}}},{{<!!!<<!!!!,{!!!>!>!!a>},{{<>}}},{<'"a{a}{!'e!!"u'u"!"o!!!>,<i">,<!!!>!!!!<u}!>,<}<!!u>}},{{}}},{{{{{<!!!!a!!u<!>},<,e!!!>iu,>,<'a,uu!!'}!!!>},<},a<!!!>e>},<>},{<{'>,{{}}},{<a!>},<!>,<!!,,u!>},<!><,a>,{}}}},{{{{<eu!!!>},<>}}},{{<!!''!>},<}o!!{>},{},{<>}},{{{{}}},{<}!}u!,,!!!!u!!i}!!!><'!!>,<eo>}},{{{{}}},{{{<!'!!"!>},<{!!!>!i!{e!!>}},{{}}},{<!>ua<<!},!"!>,<!!<!!!>'e<a>,<!!!>!,!u!>,<}"<e!!'!!!>},<!!u!<a>}}},{{{{<{!>,<"!!io!}ei,!!!>o,!>!!}!>,<<'!>,<!!!{>},{}},{{{<!>},<!!"!!!,i!!oe!!}{!>o"!>!!!!,a'!>,<>},{{<i!!i!>},<}!!!!!>a}!!!!'}!!"a>,<!!!>,<e!!!!!>!>,<>}}},{{{},{<}!!eu"eii>}},{{<!!!>},<>}},{{{<{'!>},<!!!>{>}}}},{<"o!!!>i,!>},<oo}!!}<!>},<<>,<a!!!!!<>}},{{<,,!>},<e<!>!!!!}i>},<i'!>,<>}},{},{{<,<"!!!!!!!!!>!'u{>,<{>},{{<>},<{o!>,!!{!!<ooi!!!>,<!>,<!!!}"e!>,<!!">}}},{{{{{<au>,{<!>!>,<"e!},>,{<eo},'!!>}}}},{<e!!>,{<"!'a{!>{i,!!!>,'!!!>!!!i!i!!!!o!>},<i!!!>>}},{<{!!,!>!>},<"!>,<uau!!,i!>},<o!>,<">,{{<',i,!!!>{}oi>},{<ee,!!!>!!!>ai!!!>!>!!'>}}}}},{{{<'!>,<i{!>},<!!i>},{{<a!o!>,<!!!>"!""'!!"!>},<e,e'!>},<!!>}},{{<<>},{<u,!>!!>}}},{{},<'"!>a>}},{{<eo!<'!!'>},{{{<i}<<"!!!>},<e'!>!!i!!"e<!!o<u>},{<!>,<o!e"!!!>io!!,,!!!!!>{!ooo<,a>}},{},{{<!!!>o!!"e'!!i<!!!><!!<o>}}}},{{{<<e!!!>"i!!u<'!!a!"!!!a"io,!>},<>}},{}}},{{{{{<!!,oe>},{{<u!!!!!>}}!>},<!>},<!>!!!>,<!!>}},{{}}},{{{{<'>},{<uoi<u!!e{>}},{<e!!!!ao}!!!>,<'}o!!""!!!>>}},{<uieoai"a>}},{{},{{<,!}>},{<!>},<u'!{!>},<{"a,{{}auo!!{">}},{{{},{}},{<!!!>,'!>{!!!>!!!!u{!,!>!!!>!!i!!o!a,>,{{},{<!>,<!>,<!>,<"a"<,o>}}}}},{{{},{<!e!!!><!!}>}},{{<!>},<o>}}}},{{{<!>,<{i!!'!!!>ii,}>,{<ee!!!>},<o>}},{<!!!!!!!!!>!!{'ao>}},{{{{<!>},<!>"",!!!>,'!!!>}oe}},}!>,<>}}},{<!!ie'!!'{i!!i<}'o!!}<>}},{{{<<aeo!!,a!!ui>}},{},{{<'!!<{!o!"!!!>},<!!u!!!>>}}}},{{{<!!!>!!!>},<!!!>},<!>},<!>i!">,{{<!!'<!>},<"u!!!>!!!!!>'>}}},{{{<!>,<}!!!!'!!!!e!>!>},<!!a!uo<aa!!ao,o>,<!!!!e!!!>iu'!!aa!!>},{<'o!!!>{!!!!!>!!}!i!!!>!!!>!!!>!}a}!!"!i!!!>!!!>>,<"'<{!>,<!>,<!!<}!!!>!<i!!"!"!>,<!>},<<}a>}}},{{<e<>}}},{{{{}},{{<,!>,<}!>},<!!!!a{a>},{<i,a!!!!!>i!!ao!!!>>,<!!!>>}},{{{<>,<eu"<',!>}!!{!!oa!!!>!u"'!!!>,<!>,<>},<,ee'}'!!uo!!!>,<}!!'<u{>},{<!!!>!!!>e!!!>},<!>},<"!>},<!<aa!!!{}"!>!!,a!>,<!>},<>},{{},{<!o>}}}},{{<!!!>}!>!>,<!>},<<!>,<!>{}<!a!'!!i!aa"{>,{<!!i!!!>!!ia!>'!oa>}},{{<o!>,<"!!!e!!<<!>,<!>o!!i>,<!e!>!>,<o<!!!>o!>},<!!!>u!!!>!!>},{},{{{<"!>,<oao!>,!!!!u!e!!!{}u!!,!!}!!!>>}},{<!!,ei!!!>!}!>}!!ua!>!!!!!>!!!>"!'!!!">,<,!!!>,<e!ai!'!>,<,{>}}},{{<a,!!!>,<a!!!>'i!>!!!<!>},<,}!!!!!!o">,{<!!!>,'e'!!!!!a!!i!u!>},<<'!!!>}e,>}}}},{{{{<{e!a!>},<ui,!!!!{>,<uia!i}aoa<<>}}}}},{},{{{{{<<!!'!!,>},{{<<}"u!!!!!>o",!>},<!>},<a>},{}}},{{{<!,'!!<!!!>u!>,<!!!>{!>},<>}},{}}},{{{{}},<!<>},{{{<i!{!>,<!>!>},<}a!>,<a>,{<<!>},<!>},<!!'!>!>!!!>>}},{<>},{<!!!<"!!<!!!>!!!>,<!>},<<!>},<'>}},{<!{<!>,<a!!ae,!!!>'a!!!>'"!!!ue!!>,<a<u!>},<{{!!!>o!!!>i{!,>},{{<,!!!>},<'i!>,<u">},<'!>!>},<{!!{!!!>!>},<o!!ui!>},<!!}>}}}},{{<,"<e{>},{<!>,<!u!>},<>,<u<!!}o>}},{{{}}},{{{{<a!>},<!!!!!>aeoo"!>,<>},<e,!a!!i"ee}!>!>,<>},{},{}}}}}},{{{{{{{<u!>!!',!!!>},<i!>aia!!!!'!>,<">,<!!!>!>,<!!!>!!ie!>o,<>},{<'!!e"!!!"!,">,{{{<<!!uu>}},<o<i!!!>,>}}},{<!>ueo">,<i!>},<o<>}}},{{{<!!!!!!!>!!!!!>,!!!>u'!iaa<uu}>}},{<!!'o{!>!>!<'!>},<!>},<!!!>!{o'!!!>>},{<e!u!>,<!!!>!"!!e}!>},<,i<aea>,{<"!!!>!!!>!>},<}>}}},{{{{{{}}},<,!!u!>i}u!>,<!!!><!>,<i{>},{{<!>!ai!u>,<!>,!>},<<!!!>i!>},<"!!u!uu!!{>},{},{<}!!,!!!>i{o"a!!'ioi>,{}}}}},{{{},{<i,{!!!!"!{o!>,<ou!!!!'"!!o>}},{{{<i,!>!!!>,!>,<a!>},<!!a!!!!!>,<<{!!!!>},{<!'!>>}}},{<>}}}},{{{}},{{<,>,{{<!"a!>,!>,<'a"!>>},{}}},{{{{<,,e}}i<!!!>{ia'o!>},<a<>,{}}}}}},{{{<"!!!>"">},{{<!>},<<"a!>,<<{!>},<!!,e,!!!{>}}},{<a",a!!!i!>},<>,{{<oe!!!>!<eo'e!'!!i,i{!!!!!!!>,<!>,<!!{>}}},{{<!o,!!oi!>,<!!'"{!"!!u>},<'{!!!>!>,<,u}!>!>},<!!>}}},{{{{<!>,<!>!!!>!!!>o!!ae!!!!!!!!!>{!>},<!!!>a'au,>},{{{<,!!!>,<!>},<'>}},{}},{<eea!><,>,{<!!!!!>!{!u!>,<u'{!!}!!!!!>u>}}}},{{{{{{{{<!>}"e!>},<!!'u}>,{<u!o!a<e!!"o!!!!!!"!!}a>}}}},{},{<u}u"!!!!<i!!i}>}},{{<'{!!'!!!>!ii!!o!!!>a!>},<!iu<{a>},<>}},{{<!!<!!!>a}e!>,<!!!!e,,e!<>},<',e!u!!u>}},{<>,<e,!>,<!!uui!>,<>}},{{{},{<a!'!!',,"o,>}},{<o,!!a>},{<!>},<{!!!!ai!>,<!>,<u!!i!>,<!!<!!!>i}!>e>}},{{<>,{<,'!uu!!!>,!o!!!>u{!!!!!ea,e,>}}},{{{{}},{{<{!>,o!>!>},<,<,!!!><"}''oa!!!>!>>},{{<{!!uou!!<i>}}}},{{<!!!>,<!'a!!<>},{<!i!!!!!>>}},{{<<"}!>},<"{o!>},<'!>ie!!a!!a"o!>},<!!!>>,{{{<!!i!>,{!!!!!>!!e!!!!i!>,<>}}}},{<aa!!,u,e>,{<!>!>,<<!!!>!<u,>}},{{},{<}io{!,!!>}}}}},{{{{<""'!!!>!!!'{'u!i<>},{<a,e!!o!!!!">}},{{{<u}a!>},<!>,<!!a!e,<!!ei!>,<,a!!!>,<">}}}},{{{}},{{{<,<ei!!!>u',"!!o'!!!>>}},<!>},<"e,<!!!>!}!o!>},<!!iuo{!>,<u!>},<>}}}}}}},{{{},{{},<!>},<ia!!!>,'!u>}},{{<au'i!!u!!!o!!>,{}},{{<!>!>,<!!e!>e{!!}!!!>"i!!!<>},<>},{{<!>{,!!,{!!!>"!!!ea!{u!>o<o>}}}},{{{{{}},<!!!!!!!e!>,<!>,<{<>},{{<o{a{{u!!">}}},{{},{{<!!!>,<{!!uu!!!>{>,{}},<!!<e!i!!!{!!!>!!"<,<!>,<!>},<>}},{{{{<!!!!!>'oo!!!>,o>,{<!!!!!>!>,<,!>},<'!>,<ioa>,{{<!!<>},<'i!>a'i!>,<}!!'!>!!">}}},{{{{}},{<!!!>>}},{},{{<"u!!u!"!>,<u>},<u!!!>!>e<<u<!>},<a<!i",o!{!>,<,>}},{{<!>,<!!!>}!!!>{oiaou!!}eu!!i">},{{{},<!>},<>},<"a'}a!>{ao!!!>!!!>!>!>,<!!!>i!!'eo>}}},{{<!!io>}},{<!}e!">}}},{{{<!a!!i!!e!!!!!>o!>},<!,aa,i"o!>,<e,>},<a!!{<!!!>!!u!>},<!o{!!!>!>,<!>,<{e>},{{<>},<o!oo>},{{{<,!>,,,o'!o>,{}},{{},{}},{{<!iueieo!!!>!>,<}!>},<'!>},<{!>,<ii>}}},{{{}}},{{<o<!>},<!!,i!>!><!,e!>uo"e}'<>},{{<,!!'!!!>!!eo!>},<o!>,<!!'oe!!!'ea>}}}}}}}},{{{{}},{{{{{<oeo,!>},<!!}{!o<!>},<!>!>,<oo!>!!!!>}},{{},{{<>,{<!!!>a{,'"!!a>}},{<}!u""<}ei!!<'e{>,{<i<i!>,<u>}},{{<,!!a,!!!{,}',u"a!!!>{<iaa>},{{<!!{a'!!!a!>},<u!>,<!>},<!!iiii!!!>,<"!>,<}!>,<ae>},<}"!>!!!>{!!i!'aa!!''>}}}}},{{<}!>,<',aa<!!!!<!!>,{<'!!!>'a!!!>!>,<e<!!a,,<"!!>}},{{<"!!!!!>,!>},<!>>},<{{!>},<!>,<{!!ee!i>},{}},{<!>!>,<!!!>},<,,!>,<!!'!}!ueeueoaao{u>,<'i}}{!>},<">}},{<>}},{{},{{{{<u>}},<!>},<!!i'{!>,<!>,<<u{{!>"!>,<!!!o!>,<!!"e!>},<>},{}},{{{<,<!!!>!{!>},<<!!!>'!>},<o>,{<,!a<u!>}!!!!!>!!!>>}}},{{<}!>},<!>},<u'!>e<eo,!!!>!"!!ao!ua>}},{{<a!}'!>},<}'oa!oa!>},<!,a!>u!>a'e>},{{{<!!!!e!>{>},{}},<o>}}}}},{{{<iue!>},<>,<!><,u!!!!!>ae<{{>}},{{<!!!!,!>!>!!!!!>!!'!<!!oo!>,<!>,<!!i!!!>>},<,,!!}!}!>o">},{}},{{{<i!!eio{{!>,<}>},{<'uou!a{,'i!!!>!>o{>}},{{<"!>},<!!!!!!!>,>}}}}},{{{{{<'!><!>,<au!!!io!!!>!!!>},<!>,<!!!>!>},<!!!>}!!>},{<"!>},<!i!>},<,'!!{i!a!!!!!>a"!!!!a'u!!>}},{<},,!>},<e!!!>"!>},<<u>,{<>}}}},{{<,<!!!>}<!oi!>}'!>,<'i!>>,{<!{i!!!>uo!!oie>}}},{{{<u'{>}}}},{{{{{{<a!!>}},<a!!"'!!i,,!!uo!><e!!!>ui>},{{<i{o!!!>a!!!>u!!{ai>,<!>!!!i"!>},<a{}!>'!!!!''<ae!>a!!!>},<>}},{{<ea'e!>!ao!!!>>,<i!!!>!>!!!!!><u!>}!>a>}}},{{},{},{{<!!ue!>},<'>}}},{{{{{<!<<<,"o!>,<a<!>},<,>},{<u!!!!!"!!!!!!"!>},<!>!!<!!!>,<!a'!!}!!>}},{{<!>},<!>},<!!i{!!!>!>o!!"u!!o>},{{},{}}},{{{<"e"io!!i!>,<i!!!!o"',>},{{{<!>},<!>},<e!>!>},<!>},<!!,!!}<,<>}}}}}},{{<!!!>,<!!!'a!>,<,"!o!!!>!>'>},{<}e>}}}},{{{{{},<{o!>,<o{,"i,!!e!!e!>},<!!a}!>},<>},{<!>!>},<'!>},<i!>,<u!i'!!!>}!!!>!!,oo{>,<u!>},<,{i!>!>,<'u!!!>,<i>}},<"!>,<!!,,'!!!!i>},{{<u!>i">},{<'u'''!!!>e!>!!u'!>,<!a!"!!ua>,<"!}<u'eo!a!>,<"}!,}a"!>},<>}},{{<!>}e!!'!!!>>},{<!!{!>},<>}}}},{{{{{{{}},{<>}},{}},{{{{<!i{!{!!!>"a!!o!!!>'eo!>},<!>!o!>},<>,<a!"!>},<!!}!u!!<!!!!,a'<i!>,<!!"!{o>},<iu{!>,<!"!u<>},{<,i!>,<,}!>},<!><{!!'!>},<>,<!>!u!!!>!!!!",!>,<!{}i!!!>e!!e>},{{},<!>},<!>},<'!!'!!!>!>},<}<!!"!!!>'!>,<{>}},{},{{{<!!e}au",u!!!>}!!u,}!!!>'!!!!!>'!!!>>,<!>,<oa,!}"u!>!!o!!a>},{{<!>},<!!{'o!>oo!>!>!!'e!!u,>}}},{{}},{<!>,<"!!uu!>!!eu>}},{{{<!>},<u!o"'!!!>!!ue"ea!}}>,{{<!>'>}}},{{<!>},<!>},<i!!o!>},<ia}ee!!!!ao!>,<!>,<ua>,{<!!!!!>!!!>u,<!>,<e!!ea<>}}},{<'<!>ou'!ao,>,{<a!>,<!!!!i>}}},{<!>,<"!o!>,<,e!>,<<"!>,<",<a>},{}}},{{{<>}},{{},{}}},{{{<!>e!o>},{},{<{ua!>!>,<!}!!,!!!>i'<!!u!!{!>,<>,<!!!>>}},{{{{<!!!!!!!!u!!!>i!a!>!!!!i!!{<!!!!}!>,<!!oo<"a!!!!!>>},{<!!!>!!aau'!>},<!!a!!{!>},<a>}},{{},{<!>'a}!>,<!!!{!!!>"!,>}}},{{{{{<"<<!>},<o{oao{!!!>!}{'!>},<>},<,e,!!!>,<!o!ioiu!!<!>,<e>},{<!u<i,!>"}!!!>!>>}},<'eoa{'>}},{{<e>},{<>},{<}!>!!o!ue,o{"!!e'!>!!<!!!>>,{<>}}}},{{{{<!>},<!!a!>,<!!!>!!>},<!>"e!a<a"{!>,<!i}<a!>,<}!>>},{<!!e>,{<o{}!i!!<{!!!!{!o'<!>},<!>},<o>}},{{<!!o!>!!!>!>>}}},{{{},{<e,o!!!>!>"{'u!{e!>},<!o!>},<!!'!!e>}},{{<!!!>"!}!!!>o!ao'e!}!>!>>}},{<e'!>},<u}!>},<!>},<{<''!!!>u!i'!!!>!>},<!>i>,{{},<!>},<eua,{!!!!"!>},<u!>},<!>,<!,"oi>}}},{{<i,{"}!>,<e,e"!!!>}}i!{!!!!!>,<>,{}},{{<e!!!>!>,<,!>,<a}u!>!>i!>},<!!a{>},{<u}{}}!!!!!>!!!>{<ae!>,<oo!>,<a{>}},{<"<'<!!'"o!!!!i!!i!>},<!>,<!o!!e!>},<!<!!!a>,<!>u!!'!!!>!>,<{{uui!>,<"!!"!!>}}},{{{<e!>},<!!"i!!{ee!!,euu"<!>,<u!!!>!!u,>},{{<!!!!!><'!,!>ee!>},<<!>,<oa!>,<!!!>>}},{{<u!!!!!>{{i!>,<{oi!><<>},{{<'<o"!!eo!>!!!>},<>}}}},{{{<!>!'!>,<!!!>e!>!!!u,>,{<!>"u!!a{!>,<>}},{<e!>},<e!u",{{ei!>!>,<!!!"ui,>,{<!!!><!!!!!><}!!"eo!!!">}}},{{{<{,!!i!!!!!aa!>,<!>,<>},<ei!>,<oo}!!!><!>,<,!>},<o<!!!>!!!>!u!!!>,>},{{{{<i<,}ii>},<oa!>,<"eu!!'!!!>!!!!o!!!!!>,<!!!>>},{{{<,>},<'oa!!!!u}e!!}}!>,<ea{"!>!!,>}}},{{<u!!"<'>},{<!>},<}!!>}},{{<!>,<>},{<!e!!e!!o{u!>i!>,<',}e"'>}}},{<!!!>e!!}e{}'}!!>,{}}}},{{{{{<aaae"'!!"<u!>},<>}},{<!>u!!au!>,<!!<<'>,<<,o!!!!!>iie>},{{{<uo{}!>,<!>},<>,{<!ie!!o<<!!!!!>!!!!!!>}},<o!!!u!!!>i}<!!!>},<{!>,<!u!!!>,<e'!!{ieu>}}}}},{{{<!!{a!>i{u<}i<!!"!!!>!!,>},{{{}},<{a!e!>o!<!>"o>}},{{{<'!!u!!u>},{{},{<!><!e'e!!"!>>}}},{{<!!!!}{a!!!>!!au{i>},<{e!>!>},<!>},<}o>},{{<!<!>,<}e!e'>}}}}}}},{{{{<e'!i!><!>,<!!'!!<a!>,<,!!!>>}},{<!!<!>},<'iu>,{<e{!u!!!>},<<>}}},{{{<<{,!!,!!u!!}}!!u!!!>i>},{<ae!!!>'o{o"{!!!<,!!}u!!!>!u!!>}},{<}'!!!>!>"!!'},}i!>,!>,<'">}}}},{{{},{{},{<eeuo!>},<>}},{{<'"!!<e!>,<>,<a'!>,<!!!>},<!!aa!!!>eu!!!>,<i!!!>>},{}}},{{{<i!>!!o!!'>,<!>!aa'!>},<',{>},{}}},{{{{},<{!!!>,<!>,>}}},{{{{<!!!>a'!!u!>,<a}}!>,<!}!>!>,<>},<<e!>,<!>},<!,}}"!<!!!!!>!"u>}},{{}}}}},{{{{<!}!!"o!>},<!!'i}!>},<!>'"ui{a{>},{<!>},<e!!!>oe!!!><<<,<',!ee!!!!o{>}},{{<!!o'!>,<!!!e}i!}>,<!>o!!'<oa>},{{}}}},{{{<!!"'e{u}>},{{},{<ue'!>!!!!!!}!,'{i,,!,}!>,<!!!>!>,<>}}},{{},{{{<<e!>,<}a!>,<>}},{<!"!!!>!>!}{ii!>},<{"e!>},<'aooe>,<!>!>,<!!<i"!>,<!>a!!!!oa,o>},{<!!!>},<ei!>,<>,<!>},<''i!>!>,<u!!!!}!>>}}},{{},{{<a!!!>!ia!!o!!!>},<!!!>},<!'!!!>ia>,<o{!>oa!!!>}'"!!a}{!>},<!!!!!>!>,<'}>}}},{{{<"!>,a,!!!>ui!!!!">},<{<!!e!!!>i!!a,!!!>'>},{<!>},<!"e"}ue!>,<!!}}!!a!>},<!!'}!>,<!<"u>,<<"!!!>,'{i"u!>,<ou,eo>}}}},{{{{{},{{{<!>},<!{!>!!ou}!>,<i!iu!>},<<!!uo<>},<<!u,}a!>!{>},<{!!u<!>,<<!>e'!!!{<e!u!!!>!!a!>,<,>},{}},{}},{{{}},{{{{<!>},<u{"!!!!>},<!>},<e!!e!>},<!>,<io!!iau!>!!!!!>'!u>},<e!>,<!>,<<e!<u,}e"!>,<!!!>!>!!>},{{<}i!!>},{<!!"!!,,,!>,<u"!!!>,<eo}a"!>,e'},>}},{}},{{{<!!!>,<a>}},{{{{},<e!!"!!i!!'!>"!!!>!>,<>},{<<}u!>},<o'!"!!u!!!>>},{{<}!!!>},<,o!>ai{"!>e!!!>},<a>},<<iaa<!>}},"a!>},<eu>}},{{{<!!!!o'}u!!u!!'e!{!!e!>},<{!{}i!>,<u!>,<>}},<ia!!!!!!!>!>},<!!!>'>},{<!>,<<ee>,{<}!!u{ea}!<e">}}},{<>,<!!!!o!!!>}<oa"i!>>}},{{},{{{{<<!!{!!"!>,<}!!<!"i!>,<,a,i>},{<{!'<{a!>"!>},<ue<>}},{<!!!>,<,u!>!!'i!'!>},<,,>,{<,!,!u!>"!>},<{!>},<}a}'!,>}}},{{<!>!>},<!>{!!!>e!!e!>},<!!<eo!!o'!!!!!>!>,<>},<o>},{{{<!>},<u!!!>!!!>'<{<!>!!'e!>},<a!!!>u}oo>}},{<ee'a,'{!!!!!o!ooi!uu>,{<au!uu,!!}"!>,<ie<>}}}}}},{{{<}e<!>,<o!au!>},<}!!!>!!!>a}u!>},<!!!>,'}>},{{{<i!>!!!>,<!>!,!>,!eu<a}>},<!'!!!!'!!!>{,>},<u}i!>>}},{}},{}},{{{{},{<,i!!!>!!}!!!>u!!!>!>">}}},{<!{<!!!>,!>,<!>!>},<i!>},<}!!!i>,<>}},{{{<!>,<!>},<',i}}>},{{<{i!>>}},{{<ei!>,<!>!>,<a!!!>!{!>},<>,{<ae"'>}},{{<!!!>!>},<!>},<!!ia!!"'"!!o!!!>!>,<}'!><!>},<"!!!>>,<<!!i!>,<!>e'!!!>!>},<uoui!!}u>},{}},{<o!>!!!>!>,<a}eii>}}},{{{{{}}},{{<!'!>},<au,!!!>">}},{<{oi}!>!>ai!>">,{<!>},<">}}},{{{<e!!{!>},<>},{}}}}}}}},{{{{<e<!!!>!!"o!>},<>},{{{<u!!,,!>},<o!!!!,!!!>},<aii>}},<}{!{a!>uo!>>}},{{{{}},{<e'{e>}},{{<!>!!uo"o!!i'ae!>},<!!!>,!>,<i!!'>,<!>!!!>u>},{{},{}}},{{{{<!!!>'!>,<,i!!!>>,<!"e>},{}},{{{<o!!!>},<!!!>!>,<!{a!>e{,!>,<!<o{!>},<!!{>},{{{<''<!!!o!>,<!>i{!!!>}!>},<"a!!!a!>,<!!!!!"'a>}},{{<,!!!>,<!!<'}!>,<!!!>{""uu!oo!!e,!>,<'!!a>},{<,",!>,<>}},{<!!i!>,<!!!!!'!>!!!>"!!,<o!!{!><!>},<}!o>,{<,!>!'!>{uo!!!>>}}}},{{<o!!}!>,<"ooi>},{{<iiu,!!o!>,<aa!e<'>,<!!!>,<u!i{u!!!>},<!!!!!>,<!>},<o>},<!e,}'oe'i!>!>e>}}},{{<!><'!>,<i<i'!!!!'<!>},<aoa>},{{<!!!>>}},{{},{<e!!{'{>}}},{{{{}}},{{<e<{i!>},<,!!!>"!>'a!!''>,{<,!>},<!>,!!"!>!!!!!!!>"e!!o!!!>a<!!{!u!>,<>}},{{},{<!!"!,!!!i!!!>!!o!>,,{!<!!!>"a"u!">}}}}},{{{<a<>}},{{{<!><{!>},<oo!>},<}}!a{!!!!,!>>},{<!!!"'!!!>ueu!>,<!>,<!>},<e!!!><>}}}},{{{{<'a!>},<!!!>u!!!>!!!>},<!!'"}a>},<!!'{>}},{{{},{<!>!!!>!!,u<i!>!>},<,'!>},<i,>}},{{<,{a{""!>,<!e!!!>!!,!>}'<}>},{<o!>oa!>},<aa!!oe{!>">}}}}},{{{<{,u}u<}"!>},<!e>}}}}},{{{{{},{{{{<!>,<>},{}},{{<<>}},{{<o!e!!'<}!!!>iae!>,<>}}},{<>}}},{{},{{{<a'!>},<>},<!>!!!>o!!o!>,<>},{<<a!>},<>}}},{{{{<!>},<!!e,i!!!>,<u<!>},<o<'<!<!!o{!eo>}},{{<oo!>a"o!!!>u!>},<!a'!!!!!!'!i>},<!!"{"!!!><>}},{{<!>,<>},{{<!>!!!>ea!>},<'<{io>},<!!!>!>,<!!!!i{!!!>!}!>!!!>,",a<a{!e}>}}}},{{{{{{{{<!>,<!!''!>},<{!!{!!!>!!"!>},<a!,<u>},{{{{<>},<,<o!!!>">},{{{{<u!uu!!<!!!!}>},<!!!>,'a,{!!!!iie,!!!!>},{<}o'o!<!!!>u!!,<''!!!!>,{<}'"o,u!!!><u!!!>},<!!!>!}!!!>!!<">}}},{{}},{<!!!>"!>},<!>,<e{oi,>,{<!>!!!>!>},<!!,,!!}u!>!!!!!>,<"!!!>,<,!>,<ie}!>,<i{>}}}}},{{<u}a!>},<!!i!"<">},{{{{<{'{!<!>,<!!!>>}},{}}}}},{{<a!!!>>}}},{<!>,<!>,<!!!>"!>,<i!!u,}{>,<'}!!!"{!>},<!>},<!!!!i!>},<}a!>""!>,<!!!!!>u>},{<!>,!>,<ie<a!!!>u"!>,<>}},{{{}},{<}!!a!e!!!>,!!!!!>>,{<!>{,,!,!!o{}''!>},<!>,<!{"'oo!>>}},{{{{}},<!>},<}ai"!>},<!!{!,!{}''o!!{!!!>,>},{},{}}}},{{<!}a{i>},{{<}!!!>,<!>,!!!>"!"ieia}!>},<'!>,<i>,{<!>,!}!!!!o{a''!>!!!>>}},{<u!!a!'!!}i!!u'!!,,,!!!>{o,>,{<ae!>},<"u,!!!>},<i!!!!!>},<!>},<!!a!!>}}}}}},{{{<!!,i!!!!ie>,{<!>},<!>o!!!>!'}<oe!!",!!iu!!!>>,{<!!<!>a','"!a!!!>i!e{o!>!!'!>,<>}}},{{{},{<<<>,{{{<ai!!!>!!i{e}eia"!>},<'!>'!e>},{<<,!!>}}}}},{{{},{<,i<}<!!"!>}>}}}}}},{{},{{<'>},<!!!!!>!>},<}>},{{{<e!>e{<}!>,<<o>}},{<!>,<e<o!>!""!!!>au!>},<o!!!>{!!a}e{!!!>>}}},{{},{{<!!o!>},<i>,<!o!!oae"!!<!!>}},{}}},{{{{}},{<!>},<{,{{!',a>,<<,!>,<}!>},<!!e!>!!uu",i<i<u!!">}},{{{{<!!aoa!>},<e{}!>},<!,!!u}aa>},{}},{{{<!!!>i'!oa!a!!a}'}!!!>e}>},<<!>,<u'!!!!{!!"<!>,<!!!>}}{u!>,<<"!!>}},{{},{<i>}}},{{<',!!!>!!!>!>,<>,<i!>aeoao<<!>{!>,<>},{{<,u!!!!e!>>},{{{<u!>},<!>},<!>!>},<!!}{,i<!>!!!>""o<>}},{{<}>},<!>,<}!!!>},<!>,<i,{!>,<"uo!e!!<!!!>}!>,<>}}}},{{{<,!',u!<,!!"ie">}}}},{{{{<!!!><!!<ae<!>>},{}},{{{{{<ui!>!>,<!>{,e!!ee!>,<e!i>,<!!!!!>{aio!!},>},<!!<"!!!!!!a<ou,>},{<!!,!!!!!o!>!>,<!!e!!!>,!>,<!!aaii!>'<!!!>!>>,<,!{!!!!!>"io>}}}}},{{<<'!u!>!!'{!!,!!!!i!>}!>!!a,!!!>,<a>,<!!!>!!!>"!!!>'}!!<<>},{{<oi<!,<!>},<<e!!>},{<"a}!>>},{<o!>,<<"i<!!!!!>e'e}i>,{}}},{{<oei!!,!!!>},<,}{!!o>}}},{{},{}}}}},{{<u!!!>oo>,<'e<"!!>},{{<!!!>{>}},{{{{<}o!!!!"{i'!!!!i>},{<u!'}<!!i!!i,i!!!>!a!!e">}}},{<!>},<!>,<'u>}}},{{{{<{{i!>},<>}}},{{<o!!a<>,<!!}!!{!!!>,<{!!!>,<!!u!>,<!!!>,<!>>},{<{o!!<a"<!>,!!!>,<!>!!,auo}!!!>!!}!!">,<!!<,">}},{{<{!>ei'ie!>},<}!!{e!>},<!>},<!!!><o>,<ie,},!>},<{!!<!!!>e">},{<!>"!!>,{}},{<{i{u!>},<o!>},<!>},<>,<{!!!!!>!!i!!!!!>!!"{!>},<<<'o>}}}},{{{{{<ei!>},<!!!>!!!!ia{u!!a}}i"!>},<ii>}},{{}},{<!i''!!!>!!}!!'!!i!a"!!>,<i}!!"aa!!!>!>},<!>!ii!!!>u,}>}}},{{{<u!!!>{'e{ai"!!}!>},<<!!!!!>e!!!!!>!>,<">,{<!!!!!'}!>,<'!!!>}"<'!!!!!>o!!!>i<"<>,{<e!>{!!!>}!>,<}>}}},{{<u>},{<i!!e!!e!!!>},<!!"e'{>,{<!!e!<>}}}},{{<u>}},{{},{<!>},<!!!!,'!>"ie!>},<'u>,{<!>"e!><{}!>,<!>},<!>},<!!!>}u"i<!!aa{>}},{{}}}},{{<!a!"u'"!!{!>,<!!,!>oe!>,<>},{{<u!!!>!!!>i!!!>},<a,!>!>,<{!!,i!>},<!>},<>,{<{!>,<{!!!>,<{<o>}},{{<i"!'ai"!!oa!>,<e!!"!>},<!!!>!>!!"!!!>!>!!{>,{<!"!a!!!>!>!a!!u>}},{{{<e!!"<u'!!!!!i!!'<!!!>,ai!!}!!!>!>},<!!!>,<>},<!>,<ii,!>}!>},<>}},{<!!!>},<>,{<au!>}!!,u>}}},{{{<!!!>!>},<!>,<!>,<!o!>,<!!!!i!a!!"i>}},{<i!!i!!!>>},{{<u!!ai!oau'a,'{u>},<!!"!!!!>}}}}},{{{{{<a!>u"}""!ei<}o<!>,<>,<'>},{{{<>}},<!>,<!>},<}!{,!>,<!!{!{!!u<!!!>!oo>},{{}}},{<u!!!>!!'u,!!o"!>,<}i">},{{{<!>,<",'!>},<"{ai!!',!>a>}},<i!!!>},<i!>},<ei!{!!<{!>},<'!>,<{!!!'{o<ue>}},{{{<io!>!!!>},<},io!>,<}!!a}o!>!!!>,!!!'>},{{<!!!>!!!>"o>},<'!!}>},{{{<!>">}},{<!!!>e!>,<'{!>}'!<u>,{{}}}}},{{{{{<,!>},<!,'e'!>,<i!"<i!>aue'}>}},<!u'!!a!>"!>},<u!>,<!"<!>,<i!>},<!>},<!!oa>},<!>},<o{!>},<>}}},{{},{{<!>},<!>u"},!><<a!i!!u>},{<u,a!!<e<{>},{<!>},<!>,<}<u!!!>'>,{<u<}!>},<e!><u!!!!!>!>!>},<>}}}}},{{{{<!!ae>},<>},{{{<!>},<!>},<e'!!u!>,<!!!>!!!>{',iou>}},{{<"{{!!!>},<'}i!!a!!!>!>,<i!<>},{{<>},<!!!o>}}},{{}}},{{{<!>},<!!!>u!!,!!!!!><>}},{{<}!!"!>},<!>},<!!a!!!>a!!!>!!!>a!>},<"iu>},{<"<<!!{!!!>"!!a>,{<!>},<!>,<}o!!!!!>"!>},<!!eua}ie>}}}},{{{<!>!>,<ii!!e!e'{i!!oo!>},<!!!>}{i<u>},<!!<!!}"!!!>a"ui}<>},{{<,!>,<iia'o!"!>!>,<'u!!!}e}e>},<!>},<i!>},<eu!!!>!>!ao!!!>'o!>,<!i{!>,e>},{{{<!!a"!!<!>,o'>}},{{{<i!>>}},{{<<<!!!o!!,,o<ai>},<!>,<e,!!!>,'>}}}}},{{{<',!>u<}!!u'!>},<ai!!'>},{}},{{<<u!!!>!!!>{!!!>,!>,<!>},<!}!!!>!!!>>},{{<}",!>},<!>,!',!>!!<>}}},{{{{<{>},<!!!!<{!!!>>}},{{},{<,<uu'{">}}}},{{{{{<!!!>},<!!}>},<!>i!>!!!!!>!!"!>},<}!!!{!',o>},{<!!!>a!!!!!>},<!><o'{!>}!!<"!>},<!>},<!a>}},{{<!u'}!!}!!!<,a"a!>,<u!!">}}},{{{<i!>},<!!'}>,<<"u!>!>!>},<!!!>e!!!>u}>},{<!>},<"!>,<o!>},<!!u<}>},{<e,oi'!">,{{<}"!!!>},<e!!!>a!!!!!><e!!!!!!!>}!'i!o>},{<o!!"eu<u,!!e!!!!!!!e!"a!',!!!<ee{!!"o>}}}},{{{{<!>,<">},{}},{{}},{{{},{<!!>}},{{<{a!!!>,aa!!!>!>},<!>,<}}!!!>!>},<!!'!!!"au>},<!!!>!}!!!>,<a'!>o'}!u!>,<',!!oe!!"!!!!>},{{{{<!!a<}!!",,!iua!>},<!>",a'>,<!e>}},<{!!!>!i!!!!''a!>},<!!!>!!u,e,'>},<!>oi!"!>,<!>},<,o"e"o"!>,<!>>}}},{{<i"'!!}"}!!"u{!{,'u!!>,{<'i!!ea>}},{{<>},<!>,<!}!o!>,<"}}!>!>o>},{{<o'!!!!{>}}},{{{<o,'!!!>"<!>},<!!"ie,{'{!>},<,a>}},{{}}},{{{<o'!!}a!!>,{<u!>{u{uu!'!>,<i!!!!e!>!>},<<!!!>,<a,a>}},{{<e!!!!"'!>},<o!><>},<!!i!!!>!!!!!><o>},{{{<"u!!a!>},<}!!!>{!>,<>},<,{!!a!!>},<e<!>o<,!!!>i!!!>!!!>},<}i!>},<!>""!!>}},{{{{{{<{>}},{{<oi,'!>},<>},{{<!!!e!!'e!e!!e,!,!>!!!!!>>}}},{{<!!!>!!!!!!!>,<<a,aa!>},<i>,{{<'!!!>!}!!'a>}}},{<'!>,<e>}}},{{<!>>},<o!>},<'e!!,!>,<!>a<!{>}},{{<!{!!'!!!>},<u!,u{,!!i!e!!'!'!>!!!>oi>,<!u!!!>!!!!!>,<!!"!>!!!!e,!!<!>,<!!!>i>}},{}},{}},{{},{<!<}<e!>,<!!!>>,{<!>},<!>},<!!!>!>,<'<{',e>}},{<!>u'}!!!>ui!!}">,<!!e!<!>,<u!ie!!!>!>>}}}}},{{},{{{{},{{<>},{}}}},{{{<"}!>!!!>>}},{{{<<''!>,<u<"!o!!!>>},{}},{{<!!!>'"<!>},<!!!>,<!>,<i!!!>,!!!>!>},<>,{}},{<,{e!!!!!>},<>,<a'!>},<!!}!!!>>},{<>,{}}}}},{{{<<{>}}}},{{{<!>}i{!>},<!>!!!>},<''!>,<u!!u>},<{i'"!!!>!!!!!>!>!!!>!!i>}},{{{},{{<"!>,<!!!!!!!>,{{!!ue}!>>},{<!!}!>,<{!>'!>},<o{<!>},<!!!>",,!!u!!"o>}}}}}},{{{<!>,<a'i!>,<>,<!!{,<!>},<}e>},{{},{<,!!e>}},{<!!!>,<!>,<'e},!!!>}!>ei{}}!!'{!'>,<,<o,!,iu"}ue>}},{{<a!>"eo{!>,<,!>,<!!!!a!>,<'aai!>!>},<i'>},{{{<i!!!"{i!>,<!>,<!>},<>},{}},{{{{{<!ao!,a}!"!!!ee!>}!!!>>},<a,!>,<,!>},<a!>,<<"!!'">}}},{<!!'!!i!>!>,<>,{}}}},{<o!>},<!'{!>!o!>},<}!!}a!!!>>}}}},{{{{},<o{iu}"e!!!>,!!"o!>},<!!!>"!!a!>},<<!!<,>},{<,>,{<!>},<!!'<"i!!}!>},<!u<o!!!!!>,<>,{<u<,!!a"<!>,<!!!o!!aa}i}e}>,{}}}}},{{{{},{<!,u>}},{{<!!i!>!>,<!>},<,!>!>,<e!!u>,{<!'a!!!>,<!!!!,o!{!!i>}},{{{<!!"o!!!>i{"!>o!!!!!>>}},<<!!uu!>},<'ou<aeeaie!},i>},{{{<!!'a>},{<!>,<!!!>eae!>,<ou!!u}>,<>}},{<,i"u}!!'i'!!!>{!>},<!!{o!ii!>">}}}},{{<!>'ua"'>}},{{{},{{<!>!!!>a<'>},{<i!>,<!>,<!!!>,<!>},<a,,>,{<>}}}},{<,u!>aa{aeo!e,<>,{<!!>}}}}}},{{},{{{<''>,<}a!>},<ao!>},<{!!"!!}e}u!!a!>},<{!!u{>},{<ueo>,<}!<>}},{{<aeu!!i}!o!>},<!!!>i'}"{,<o>,{<ii!!!>},<>}}},{{{{<!>,<!!'o"o!!!>i{,i>}},{<<"o,o}!!!aa"e!!!>o>,<{!>,<ua{a>}},{{{{{},<'ui!!!>,<!!i>}},{<e<}!e!!u>},{<!!!a!!!>oo!!,!!!>,<o>}},{{<'uo}o!!<e!!!>},<u,"a>}},{{},{{},{<!>>}}}}}}}}"""
def solve(data):
    output = 0
    group_level = 0
    ignore = False
    garbage = False
    for ch in data:
#         print('ch: {}\noutput: {}\ngroup_level: {}\nignore: {}\ngarbage: {}'.format(ch, output, group_level, ignore, garbage))
        if ignore:
            ignore = False
            continue
        if ch == '!':
            ignore = True
            continue
        if garbage:
            if ch == '>':
                garbage = False
        else:
            if ch == '{':
                group_level += 1
            if ch == '}':
                output += group_level
                group_level -= 1
            if ch == '<':
                garbage = True
    return output
            
assert solve('{}') == 1
assert solve('{{{}}}') == 6
assert solve('{{},{}}') == 5
assert solve('{{{},{},{{}}}}') == 16
assert solve('{<a>,<a>,<a>,<a>}') == 1
assert solve('{{<ab>},{<ab>},{<ab>},{<ab>}}') == 9
assert solve('{{<!!>},{<!!>},{<!!>},{<!!>}}') == 9
assert solve('{{<a!>},{<a!>},{<a!>},{<ab>}}') == 3
print(solve(data))
def solve(data):
    output = 0
    ignore = False
    garbage = False
    for ch in data:
#         print('ch: {}\noutput: {}\ngroup_level: {}\nignore: {}\ngarbage: {}'.format(ch, output, group_level, ignore, garbage))
        if ignore:
            ignore = False
            continue
        if ch == '!':
            ignore = True
            continue
        if garbage:
            if ch == '>':
                garbage = False
            else:
                output += 1
        else:
            if ch == '<':
                garbage = True
    return output
assert solve('{}') == 0
assert solve('<{!>}>') == 2
assert solve('{{},{}}') == 0
assert solve('{<{o"i!a,<{i<a>}') == 10
assert solve('{<a>,<a>,<a>,<a>}') == 4
assert solve('{{<ab>},{<ab>},{<ab>},{<ab>}}') == 8
assert solve('{{<!!>},{<!!>},{<!!>},{<!!>}}') == 0
assert solve('{{<a!>},{<a!>},{<a!>},{<ab>}}') == 17
print(solve(data))
data = [63, 144, 180, 149, 1, 255, 167, 84, 125, 65, 188, 0, 2, 254, 229, 24]
def solve(length, lengths):
    data = list(range(length))
    skip = 0
    pos = 0
    for l in lengths:
        if l == len(data):
            f = (data+data)
            pre = f[:pos]
            rev = f[pos:pos+l][::-1]
            post = f[pos+l:]
            f = pre+rev+post
            data = f[l:l+pos]+f[pos:l]
        elif pos+l > len(data):
            f = (data+data)
            pre = f[:pos]
            rev = f[pos:pos+l][::-1]
            post = f[pos+l:]
            f = pre+rev+post
            data = f[len(data):len(data)+pos] + f[pos:len(data)]        
        else:
            pre = data[:pos]
            rev = data[pos:pos+l]
            post = data[pos+l:]
            data = pre+rev[::-1]+post
        pos = (pos+l+skip)%len(data)
        skip += 1
    return data[0]*data[1]
assert solve(5, [3, 4, 1, 5]) == 12
print(solve(256, data))
def run_once(lengths, data=None, skip=0, pos=0):
    if not data:
        data = list(range(256))
    skip = skip
    pos = pos
    for l in lengths:
        if l == len(data):
            f = (data+data)
            pre = f[:pos]
            rev = f[pos:pos+l][::-1]
            post = f[pos+l:]
            f = pre+rev+post
            data = f[l:l+pos]+f[pos:l]
        elif pos+l > len(data):
            f = (data+data)
            pre = f[:pos]
            rev = f[pos:pos+l][::-1]
            post = f[pos+l:]
            f = pre+rev+post
            data = f[len(data):len(data)+pos] + f[pos:len(data)]        
        else:
            pre = data[:pos]
            rev = data[pos:pos+l]
            post = data[pos+l:]
            data = pre+rev[::-1]+post
        pos = (pos+l+skip)%len(data)
        skip += 1
    return {'data':data, 'skip': skip, 'pos': pos}
def get_lengths(data=''):
    return [ord(x) for x in data]+[17, 31, 73, 47, 23]
    
def run_multiple(lengths=[]):
    rets = {}
    for p in range(64):
        rets = run_once(lengths, **rets)
    return rets['data']
def get_hash(data):
    out = ''
    for x in range(0, len(data), 16):
        tmp=0
        for y in range(16):
            tmp = tmp^data[x+y]
        out += '{:02x}'.format(tmp)
    return out
def solve(key=None):
    if not key:
        key=''
    lengths = get_lengths(key)
    print('key: {}\nlengths: {}'.format(key,lengths))
    data = run_multiple(lengths)
    test_hash = get_hash(data[:16])
    print('test hash: {}'.format(test_hash))
    return get_hash(data)
    
       
# assert solve(None) == 'a2582a3a0e66e6e86e3812dcb672a272'
# assert solve('AoC 2017') == '33efeb34ea91902bb2f59c9920caa6cd'
# assert solve('1,2,3') == '3efbe78a8d82f29979031a4aa0b16a9d'
# assert solve('1,2,4') == '63960835bcdc130f0b66d7ff4f6a5a8e'
d = ",".join(map(str,data))
print(solve(d))
data = """se,s,ne,sw,sw,sw,sw,sw,ne,sw,nw,nw,nw,nw,ne,n,nw,nw,n,sw,n,n,n,n,n,ne,nw,ne,n,sw,n,ne,ne,ne,ne,sw,ne,nw,n,ne,ne,ne,sw,ne,ne,s,se,ne,se,se,se,s,se,se,se,se,se,se,se,se,ne,se,se,ne,se,s,s,se,se,se,s,se,s,s,se,s,s,s,s,se,ne,se,se,s,s,sw,s,s,n,sw,s,s,s,s,s,s,s,s,s,s,s,s,s,sw,s,s,s,s,s,n,s,nw,s,s,s,s,s,se,s,sw,se,sw,s,sw,sw,nw,s,s,se,s,s,s,sw,s,se,sw,sw,sw,sw,ne,s,sw,sw,s,sw,nw,sw,sw,sw,sw,s,sw,sw,sw,se,sw,sw,sw,s,sw,n,sw,sw,s,nw,sw,sw,ne,n,se,sw,sw,sw,nw,sw,n,nw,sw,nw,se,sw,sw,nw,sw,n,sw,sw,nw,sw,sw,nw,n,nw,nw,nw,n,n,nw,sw,n,nw,se,nw,nw,nw,n,sw,nw,nw,nw,ne,sw,nw,s,nw,nw,nw,nw,nw,nw,nw,nw,ne,n,nw,nw,nw,se,nw,n,nw,nw,se,nw,nw,nw,nw,nw,nw,nw,nw,nw,nw,nw,nw,nw,se,nw,nw,n,s,se,s,s,s,n,n,n,ne,nw,n,s,n,n,nw,nw,n,n,nw,nw,n,n,n,nw,n,n,n,nw,n,n,nw,n,n,n,nw,nw,n,se,n,nw,n,s,nw,se,se,nw,nw,n,n,nw,n,nw,nw,nw,nw,n,n,nw,n,ne,n,n,n,n,n,n,n,n,n,n,n,n,s,n,se,n,n,ne,se,n,n,n,ne,n,n,n,n,s,n,ne,n,ne,ne,n,n,se,nw,n,se,n,n,ne,n,n,n,n,n,ne,sw,nw,n,sw,ne,n,n,n,n,sw,n,n,sw,n,n,n,ne,n,n,n,nw,sw,ne,nw,n,s,s,nw,nw,n,sw,n,sw,ne,ne,ne,ne,ne,nw,n,n,nw,n,ne,se,ne,ne,s,se,n,n,n,n,ne,n,s,n,ne,s,n,ne,ne,ne,n,ne,n,n,se,n,se,n,ne,ne,n,n,se,ne,ne,ne,n,ne,ne,ne,ne,ne,ne,ne,ne,n,se,n,ne,ne,ne,ne,ne,se,ne,ne,ne,ne,ne,ne,ne,ne,ne,ne,ne,ne,s,ne,sw,n,ne,ne,ne,ne,ne,sw,se,n,ne,n,n,ne,se,n,ne,s,ne,se,ne,ne,ne,s,s,nw,ne,se,sw,ne,ne,ne,ne,ne,ne,ne,se,se,nw,ne,ne,ne,s,ne,ne,ne,ne,ne,n,ne,ne,ne,se,ne,ne,sw,ne,se,ne,sw,ne,se,s,se,ne,ne,se,se,ne,sw,se,ne,ne,ne,se,sw,ne,ne,ne,ne,se,ne,n,se,ne,se,ne,se,se,se,ne,n,se,sw,se,ne,sw,ne,ne,ne,ne,ne,ne,se,se,ne,ne,s,ne,se,se,se,ne,se,se,se,sw,se,n,se,se,se,n,se,ne,se,n,se,se,se,ne,ne,sw,s,se,ne,nw,se,s,ne,ne,se,sw,ne,nw,s,se,ne,se,se,s,nw,ne,ne,se,se,s,nw,ne,ne,se,ne,nw,ne,se,nw,ne,se,s,s,n,se,se,ne,ne,ne,se,s,se,se,s,se,se,se,se,se,se,se,se,se,se,ne,se,se,n,se,nw,sw,se,se,se,ne,nw,ne,s,se,se,se,se,se,se,se,se,ne,se,se,se,se,se,se,s,se,se,se,se,n,se,se,sw,se,se,se,se,se,se,se,se,se,n,se,ne,sw,nw,se,se,se,se,se,s,se,se,s,se,se,se,se,se,se,s,s,se,sw,n,se,s,se,se,s,s,n,se,nw,se,se,se,se,se,s,sw,se,se,se,s,se,se,sw,se,ne,s,se,se,ne,se,se,s,se,s,se,n,se,s,s,se,se,s,s,se,se,se,s,s,se,nw,sw,n,se,se,s,se,s,s,s,s,se,se,se,s,sw,se,se,se,se,ne,s,se,se,n,nw,se,s,ne,s,se,se,se,n,n,se,se,s,s,sw,se,n,s,se,nw,s,ne,s,s,s,sw,se,s,se,s,s,s,ne,s,s,s,s,se,s,s,se,n,s,nw,se,s,sw,s,s,sw,s,s,nw,se,nw,s,se,nw,s,s,se,se,se,s,se,n,se,s,se,s,se,s,s,s,s,nw,s,n,s,s,sw,s,se,s,s,s,s,ne,s,n,s,s,s,s,se,s,s,se,s,nw,se,s,nw,se,s,s,s,s,nw,s,s,s,s,s,s,se,se,s,s,s,s,s,s,s,s,s,sw,se,n,s,n,s,nw,se,s,s,s,s,nw,s,ne,sw,s,sw,s,s,ne,n,s,n,sw,s,s,s,s,s,s,s,nw,sw,n,n,n,s,s,ne,s,s,s,s,s,s,s,s,sw,s,s,s,ne,ne,s,s,s,s,s,s,s,s,s,s,s,s,ne,nw,s,s,s,s,se,s,s,s,s,s,s,s,s,se,se,sw,nw,sw,s,s,n,s,s,sw,s,sw,s,se,s,n,sw,s,s,ne,sw,ne,se,s,s,s,s,nw,sw,s,s,s,s,s,s,s,s,s,se,ne,n,n,s,s,s,s,sw,s,s,s,s,s,s,s,sw,s,s,sw,nw,sw,ne,s,s,sw,s,ne,ne,se,sw,s,s,sw,s,s,sw,s,sw,n,s,s,s,s,n,s,s,s,s,s,s,s,s,ne,sw,s,n,ne,s,s,sw,s,s,sw,s,s,sw,s,nw,s,s,sw,se,s,s,sw,se,s,s,sw,s,sw,sw,s,s,s,s,sw,nw,sw,sw,sw,s,sw,sw,sw,sw,sw,s,sw,nw,ne,sw,sw,n,s,se,s,s,s,s,sw,s,s,s,s,ne,s,s,s,sw,sw,s,s,s,s,n,sw,sw,s,sw,s,sw,sw,sw,sw,se,sw,sw,s,s,sw,s,s,n,sw,sw,s,sw,s,s,s,s,sw,sw,s,sw,sw,s,sw,sw,ne,sw,sw,ne,s,sw,sw,sw,s,sw,ne,sw,sw,sw,sw,ne,sw,s,sw,sw,s,s,s,sw,s,sw,sw,n,se,s,sw,sw,sw,n,s,s,s,n,s,sw,sw,s,sw,sw,s,ne,sw,ne,sw,sw,s,s,sw,sw,sw,sw,ne,n,s,sw,sw,sw,sw,sw,ne,sw,ne,s,se,sw,sw,sw,se,sw,ne,sw,sw,ne,sw,s,sw,ne,n,sw,sw,sw,nw,sw,n,s,sw,ne,sw,s,sw,sw,s,sw,sw,sw,sw,nw,s,nw,nw,sw,sw,n,n,ne,s,sw,s,sw,sw,sw,sw,sw,sw,sw,sw,sw,s,sw,s,sw,sw,sw,sw,sw,sw,sw,sw,n,sw,sw,n,sw,sw,s,sw,sw,sw,sw,sw,ne,s,sw,sw,sw,sw,sw,sw,sw,sw,sw,sw,sw,sw,sw,se,sw,sw,nw,sw,sw,sw,ne,sw,n,s,ne,n,sw,sw,s,sw,sw,sw,sw,sw,sw,sw,n,sw,sw,sw,sw,sw,s,n,sw,sw,nw,sw,sw,sw,ne,s,sw,sw,sw,sw,nw,nw,sw,nw,nw,sw,sw,nw,sw,sw,sw,sw,sw,nw,nw,nw,n,ne,sw,sw,sw,se,sw,sw,sw,sw,sw,sw,nw,sw,sw,sw,sw,ne,sw,sw,sw,sw,sw,s,nw,sw,sw,sw,nw,nw,nw,sw,sw,sw,sw,sw,se,ne,sw,sw,sw,sw,sw,nw,sw,sw,sw,sw,sw,sw,sw,sw,nw,nw,sw,ne,sw,sw,nw,sw,sw,se,nw,sw,ne,sw,sw,sw,sw,n,sw,sw,sw,sw,sw,sw,nw,s,nw,nw,nw,sw,n,se,sw,ne,s,sw,sw,se,sw,n,sw,sw,sw,sw,nw,sw,sw,sw,nw,sw,sw,sw,nw,ne,sw,n,sw,sw,s,nw,sw,sw,sw,sw,nw,sw,sw,ne,sw,nw,n,ne,n,sw,nw,sw,nw,nw,nw,sw,ne,n,sw,sw,sw,nw,sw,sw,sw,sw,sw,nw,nw,sw,nw,sw,se,sw,s,sw,nw,sw,nw,nw,sw,sw,ne,nw,sw,nw,sw,sw,sw,s,n,nw,nw,sw,sw,s,nw,sw,sw,nw,sw,sw,sw,sw,nw,nw,nw,ne,sw,se,n,n,n,nw,ne,nw,nw,sw,nw,se,nw,sw,n,sw,sw,nw,sw,sw,sw,sw,sw,ne,se,sw,sw,nw,sw,sw,nw,sw,nw,nw,nw,nw,sw,sw,nw,sw,ne,nw,sw,ne,sw,sw,sw,nw,ne,sw,nw,nw,nw,se,se,se,sw,n,nw,nw,nw,sw,sw,se,sw,nw,nw,nw,nw,sw,nw,nw,sw,nw,nw,sw,nw,n,nw,se,nw,nw,nw,nw,se,nw,sw,nw,nw,nw,ne,nw,ne,s,nw,sw,nw,nw,nw,nw,sw,nw,se,nw,sw,nw,s,sw,nw,ne,ne,sw,sw,nw,nw,nw,ne,sw,s,s,ne,nw,nw,n,nw,sw,sw,nw,n,nw,nw,nw,ne,nw,se,sw,nw,s,s,nw,nw,nw,se,sw,nw,s,nw,nw,n,sw,nw,sw,nw,nw,sw,nw,nw,sw,nw,nw,ne,sw,sw,nw,nw,sw,sw,nw,nw,nw,nw,sw,n,s,ne,se,n,nw,sw,sw,s,sw,nw,nw,nw,nw,nw,nw,nw,nw,nw,nw,sw,se,nw,s,nw,nw,sw,nw,se,sw,sw,n,nw,nw,ne,ne,nw,nw,nw,nw,n,nw,nw,nw,nw,nw,nw,nw,sw,nw,nw,nw,nw,nw,nw,sw,nw,nw,sw,nw,nw,s,ne,nw,s,nw,sw,nw,n,s,nw,nw,nw,ne,nw,sw,s,n,nw,n,ne,nw,nw,ne,ne,nw,se,sw,nw,n,nw,sw,nw,nw,nw,n,s,s,nw,ne,nw,s,nw,nw,nw,sw,nw,nw,nw,sw,s,s,ne,nw,ne,sw,sw,sw,nw,ne,nw,sw,nw,nw,se,n,nw,nw,sw,nw,sw,nw,nw,n,nw,n,nw,s,nw,n,sw,nw,nw,nw,nw,nw,nw,nw,nw,se,nw,nw,n,sw,nw,nw,nw,nw,ne,nw,sw,nw,se,nw,nw,nw,nw,ne,nw,nw,nw,nw,ne,s,nw,nw,nw,nw,nw,nw,nw,ne,nw,nw,nw,nw,s,nw,nw,nw,nw,sw,nw,nw,nw,se,nw,nw,nw,nw,nw,nw,nw,n,nw,n,nw,nw,sw,n,nw,nw,nw,nw,nw,nw,s,nw,s,n,se,nw,nw,nw,nw,s,nw,ne,nw,se,n,nw,n,s,nw,nw,sw,nw,nw,nw,nw,nw,sw,nw,nw,nw,nw,nw,nw,nw,nw,n,nw,nw,nw,n,ne,nw,nw,s,nw,nw,nw,nw,sw,nw,nw,nw,n,nw,nw,nw,nw,nw,se,nw,nw,s,se,nw,ne,nw,n,n,s,nw,se,nw,n,nw,nw,nw,nw,sw,nw,nw,n,ne,nw,nw,n,nw,nw,nw,sw,nw,n,ne,se,se,nw,nw,nw,nw,nw,nw,n,n,nw,nw,nw,s,n,nw,nw,nw,nw,nw,n,n,nw,n,nw,nw,n,nw,n,nw,nw,nw,nw,nw,nw,nw,nw,nw,se,n,n,nw,nw,nw,nw,nw,nw,n,n,sw,nw,n,n,nw,sw,n,nw,s,nw,nw,n,nw,nw,nw,se,n,nw,nw,nw,s,n,n,nw,nw,n,n,sw,nw,n,nw,nw,nw,nw,nw,se,n,nw,nw,nw,nw,nw,nw,nw,nw,nw,n,ne,ne,nw,nw,nw,ne,n,nw,se,nw,sw,nw,n,nw,ne,n,nw,n,n,n,n,n,n,n,n,nw,nw,sw,n,n,nw,nw,n,nw,nw,ne,nw,se,s,nw,sw,nw,nw,nw,nw,nw,nw,n,ne,n,nw,n,nw,n,nw,nw,nw,n,nw,nw,nw,nw,nw,s,nw,nw,n,s,se,n,sw,se,n,n,n,n,nw,nw,nw,n,nw,sw,nw,nw,nw,nw,nw,ne,se,n,n,nw,n,nw,nw,n,se,nw,n,n,nw,n,ne,n,nw,n,n,n,ne,ne,n,nw,nw,nw,sw,se,n,n,nw,s,nw,sw,nw,n,nw,n,s,se,n,nw,nw,n,nw,se,n,se,nw,n,se,s,n,nw,nw,n,nw,n,n,ne,nw,n,sw,n,nw,nw,nw,nw,n,n,n,sw,nw,nw,ne,nw,n,nw,n,sw,nw,nw,n,nw,n,n,n,nw,n,n,n,se,nw,nw,n,nw,n,ne,sw,se,nw,nw,nw,ne,nw,n,se,n,nw,n,n,nw,sw,ne,nw,n,n,ne,nw,nw,sw,nw,s,n,nw,n,nw,nw,nw,nw,sw,s,nw,sw,nw,n,n,n,nw,nw,nw,n,n,sw,s,ne,s,nw,n,n,nw,n,n,n,n,n,ne,n,n,nw,n,nw,n,nw,n,n,se,n,ne,n,n,n,nw,sw,n,n,nw,sw,nw,n,n,nw,n,ne,sw,nw,nw,n,n,n,n,sw,n,nw,nw,n,n,n,n,nw,nw,n,nw,n,n,n,ne,sw,n,s,n,n,n,sw,nw,ne,nw,n,n,nw,n,nw,nw,n,s,nw,nw,s,n,ne,nw,n,sw,nw,n,n,n,n,n,ne,n,se,n,n,n,n,n,se,n,nw,n,n,nw,sw,n,nw,n,nw,nw,sw,ne,nw,nw,n,nw,nw,n,n,n,nw,sw,n,n,sw,n,n,se,n,s,n,sw,nw,n,n,nw,se,nw,nw,n,n,n,n,n,nw,nw,n,n,ne,nw,nw,n,n,n,n,sw,n,se,se,n,n,n,nw,ne,n,nw,nw,n,sw,nw,s,n,ne,n,n,n,nw,nw,se,n,n,n,n,nw,n,n,n,n,n,n,n,n,n,n,ne,n,n,n,nw,n,nw,n,nw,n,n,n,n,nw,ne,n,n,nw,s,n,n,nw,sw,n,n,nw,n,n,nw,n,n,n,n,nw,n,n,sw,nw,n,n,n,n,nw,n,n,n,nw,n,n,n,n,n,n,n,n,n,s,n,n,n,nw,n,n,n,n,n,n,n,s,n,n,n,n,s,n,n,n,n,n,sw,n,sw,n,nw,n,ne,sw,n,n,n,n,nw,n,n,n,n,n,n,n,n,n,n,ne,n,sw,n,n,n,n,ne,n,n,n,n,n,n,n,n,n,n,n,n,n,ne,n,n,n,n,n,n,n,n,n,n,n,n,n,n,n,n,sw,n,n,n,n,n,n,n,n,n,n,n,n,s,n,sw,sw,n,n,n,sw,n,se,n,n,n,n,n,se,n,s,n,n,n,n,n,n,n,nw,n,n,n,n,s,ne,n,n,se,n,se,n,n,n,n,n,ne,n,n,n,n,n,nw,n,n,s,n,n,n,ne,n,n,se,n,ne,n,n,n,n,n,n,sw,n,n,se,n,n,n,n,n,n,n,n,n,n,ne,n,nw,ne,n,n,sw,n,n,n,nw,ne,n,n,n,s,ne,n,n,n,n,n,ne,n,n,ne,n,n,n,n,n,se,n,ne,n,n,s,n,n,n,ne,n,n,nw,n,nw,ne,n,se,n,n,n,sw,ne,n,n,n,s,sw,n,n,ne,n,n,n,n,ne,ne,n,s,ne,n,ne,n,nw,n,n,ne,n,n,n,ne,se,n,ne,sw,ne,se,nw,se,n,s,n,n,ne,n,n,se,n,n,ne,n,n,ne,ne,nw,se,n,n,n,n,n,n,n,n,n,ne,nw,ne,s,sw,n,n,n,ne,n,n,n,n,n,ne,ne,n,n,n,n,n,ne,ne,ne,n,se,ne,n,ne,n,n,n,n,n,n,s,n,n,ne,n,n,n,n,sw,se,ne,ne,n,n,se,ne,sw,n,n,ne,n,n,n,n,n,ne,n,n,n,n,n,n,ne,se,s,ne,n,ne,ne,n,n,s,ne,n,s,ne,ne,ne,n,n,n,n,ne,n,n,ne,nw,n,n,n,n,n,n,n,ne,n,n,n,n,nw,n,nw,n,n,n,sw,ne,n,n,ne,ne,n,nw,s,sw,sw,n,n,s,n,n,n,n,n,ne,n,ne,n,n,n,n,ne,n,n,se,ne,sw,nw,n,ne,ne,ne,se,ne,n,ne,n,n,n,n,ne,n,n,n,n,n,n,n,sw,ne,n,nw,ne,n,s,ne,ne,n,ne,n,n,ne,s,n,ne,n,n,ne,se,n,n,n,ne,ne,n,nw,n,n,se,n,n,n,n,se,n,s,s,n,nw,se,ne,se,n,ne,n,n,n,n,n,nw,ne,n,n,n,ne,n,ne,n,n,ne,ne,n,n,ne,n,sw,ne,n,n,n,sw,n,n,ne,ne,n,n,nw,n,n,n,n,n,ne,ne,se,n,nw,n,ne,ne,n,n,n,se,n,ne,sw,n,n,ne,ne,ne,ne,n,n,ne,ne,ne,ne,n,n,sw,n,sw,ne,se,ne,ne,n,ne,nw,n,ne,ne,n,ne,ne,n,n,n,s,ne,ne,n,se,n,ne,nw,sw,nw,se,ne,ne,n,s,sw,ne,ne,s,ne,n,n,ne,n,se,n,sw,ne,n,ne,ne,n,ne,ne,s,s,n,ne,se,n,n,n,ne,sw,n,n,n,sw,n,s,ne,n,nw,ne,s,n,se,ne,n,n,s,ne,ne,ne,se,ne,ne,ne,n,n,n,sw,ne,n,n,ne,n,ne,n,s,ne,n,n,sw,ne,n,sw,s,n,n,s,ne,se,n,nw,n,n,se,ne,se,n,n,s,se,n,ne,n,n,ne,n,ne,sw,ne,n,ne,s,nw,n,n,n,n,ne,ne,n,ne,n,n,n,n,sw,ne,ne,ne,se,ne,sw,n,n,n,sw,sw,n,ne,sw,se,ne,se,ne,nw,ne,n,ne,sw,ne,n,ne,n,ne,n,ne,sw,sw,n,n,s,n,ne,sw,ne,ne,ne,n,ne,n,ne,n,ne,n,n,ne,ne,n,ne,ne,n,ne,se,ne,ne,n,ne,ne,se,ne,ne,ne,se,n,n,ne,ne,se,ne,n,se,n,n,n,ne,ne,n,n,ne,ne,n,n,ne,ne,ne,sw,ne,s,ne,ne,ne,nw,ne,n,ne,ne,nw,n,n,ne,ne,ne,sw,ne,ne,n,nw,ne,n,ne,s,sw,ne,n,n,n,ne,se,ne,ne,ne,n,ne,se,ne,n,sw,n,n,s,ne,ne,se,n,n,ne,ne,ne,s,s,ne,sw,sw,n,ne,se,ne,ne,sw,ne,ne,ne,ne,s,ne,ne,ne,ne,ne,nw,n,ne,ne,sw,ne,ne,n,ne,ne,nw,sw,n,ne,n,n,s,ne,ne,ne,ne,ne,ne,ne,ne,ne,sw,ne,ne,n,ne,ne,ne,se,ne,s,s,s,s,ne,nw,se,n,ne,ne,n,n,ne,n,ne,ne,se,n,n,ne,ne,n,ne,ne,ne,ne,ne,ne,ne,sw,ne,ne,ne,n,nw,se,n,ne,s,ne,s,ne,ne,ne,ne,se,se,sw,sw,ne,ne,ne,ne,ne,sw,n,se,ne,ne,ne,ne,ne,n,ne,s,ne,ne,ne,ne,ne,ne,s,n,ne,ne,ne,n,n,ne,ne,ne,n,ne,ne,ne,ne,ne,ne,ne,n,sw,ne,ne,ne,ne,ne,n,n,s,se,ne,ne,ne,n,s,n,se,ne,ne,s,se,sw,n,ne,ne,se,ne,ne,ne,ne,sw,ne,n,ne,n,ne,ne,ne,n,ne,n,n,n,s,ne,ne,ne,n,ne,nw,se,ne,ne,ne,ne,n,ne,ne,ne,ne,ne,s,ne,ne,ne,ne,n,se,ne,ne,n,ne,nw,ne,n,ne,ne,ne,sw,ne,s,n,nw,ne,sw,ne,sw,nw,ne,se,s,ne,ne,ne,ne,nw,ne,ne,n,ne,se,n,ne,ne,ne,ne,s,nw,ne,n,ne,ne,ne,ne,n,nw,n,n,ne,ne,ne,ne,n,ne,n,ne,ne,ne,ne,ne,nw,ne,se,ne,ne,ne,s,ne,n,ne,ne,sw,ne,ne,n,ne,ne,ne,n,ne,ne,ne,nw,se,n,ne,se,nw,ne,ne,s,ne,ne,ne,ne,ne,ne,sw,ne,ne,ne,s,ne,ne,ne,ne,ne,ne,ne,sw,nw,ne,ne,sw,nw,ne,ne,n,ne,ne,ne,ne,ne,ne,ne,ne,sw,ne,ne,ne,se,ne,ne,ne,sw,ne,nw,ne,ne,se,ne,ne,ne,ne,ne,ne,ne,ne,ne,s,ne,ne,ne,ne,n,ne,nw,ne,ne,nw,ne,ne,ne,n,ne,n,ne,ne,nw,se,ne,ne,ne,ne,ne,se,ne,ne,ne,ne,ne,se,se,ne,nw,ne,ne,ne,ne,ne,nw,sw,ne,ne,ne,ne,n,n,ne,ne,nw,nw,ne,nw,sw,nw,sw,ne,ne,ne,ne,ne,ne,ne,ne,ne,s,ne,ne,ne,ne,ne,s,ne,ne,ne,ne,s,ne,ne,s,ne,ne,ne,nw,ne,ne,se,ne,se,n,s,ne,ne,ne,ne,n,ne,ne,ne,ne,se,ne,ne,ne,se,ne,ne,ne,ne,ne,ne,se,ne,ne,ne,ne,ne,ne,ne,ne,ne,ne,ne,ne,ne,s,ne,ne,se,ne,ne,ne,ne,se,ne,ne,ne,ne,se,ne,ne,ne,se,s,ne,ne,ne,ne,ne,ne,ne,ne,se,ne,n,ne,ne,ne,s,se,ne,ne,ne,ne,ne,ne,s,ne,ne,ne,sw,ne,ne,ne,ne,se,ne,ne,ne,n,se,ne,ne,ne,ne,ne,ne,ne,ne,ne,ne,se,ne,n,ne,ne,ne,se,ne,se,sw,ne,ne,ne,se,ne,ne,ne,se,ne,ne,se,ne,ne,ne,se,ne,ne,sw,se,ne,ne,ne,se,nw,ne,ne,ne,ne,ne,ne,ne,ne,ne,ne,ne,ne,sw,nw,ne,ne,ne,ne,n,ne,se,ne,ne,sw,ne,ne,ne,s,sw,ne,ne,ne,se,ne,ne,ne,ne,ne,ne,ne,se,ne,ne,nw,ne,ne,s,se,ne,ne,se,nw,sw,n,se,ne,ne,n,ne,ne,ne,ne,ne,n,s,ne,ne,se,ne,se,ne,n,ne,ne,nw,se,se,se,ne,se,ne,ne,ne,se,se,ne,ne,ne,se,n,ne,ne,ne,s,n,n,se,ne,sw,ne,ne,ne,ne,ne,ne,s,se,ne,n,se,s,sw,ne,se,ne,ne,nw,n,ne,se,se,ne,se,ne,ne,ne,ne,ne,ne,se,ne,ne,se,ne,se,ne,ne,ne,sw,nw,n,ne,s,nw,se,nw,se,ne,sw,ne,sw,n,ne,ne,ne,ne,ne,ne,ne,ne,ne,ne,ne,se,se,ne,ne,ne,n,ne,n,ne,ne,se,se,se,ne,se,se,se,ne,nw,ne,ne,se,ne,ne,nw,se,ne,ne,s,ne,se,se,ne,ne,ne,ne,se,ne,se,ne,ne,n,ne,ne,sw,se,se,se,ne,se,ne,ne,se,ne,s,ne,ne,ne,ne,ne,se,se,se,s,ne,se,ne,ne,se,se,ne,ne,se,ne,ne,ne,ne,se,ne,se,se,nw,ne,ne,ne,s,ne,ne,se,ne,n,se,sw,ne,ne,s,ne,se,ne,ne,s,nw,se,n,n,ne,ne,n,sw,se,sw,ne,ne,se,ne,ne,ne,ne,n,se,se,sw,n,se,ne,sw,ne,ne,se,ne,ne,ne,ne,s,n,ne,se,se,ne,ne,ne,se,se,s,ne,ne,ne,se,ne,n,ne,se,ne,ne,se,ne,ne,se,ne,ne,ne,ne,s,se,s,se,se,ne,se,ne,n,ne,se,n,ne,ne,se,ne,n,ne,ne,ne,ne,sw,ne,ne,ne,se,ne,ne,s,ne,sw,nw,se,se,s,s,se,ne,se,ne,s,ne,ne,ne,nw,ne,sw,ne,ne,se,se,se,ne,se,ne,se,ne,se,ne,ne,se,se,se,ne,ne,se,se,ne,se,s,ne,se,ne,nw,se,ne,n,ne,ne,ne,ne,ne,se,se,se,n,se,se,se,ne,ne,ne,se,n,ne,nw,ne,ne,se,ne,ne,ne,n,se,se,se,se,se,n,se,nw,ne,se,ne,ne,se,ne,se,ne,n,ne,ne,se,se,se,ne,se,se,ne,ne,ne,ne,ne,ne,ne,ne,se,se,ne,se,s,sw,ne,se,ne,se,se,ne,s,ne,n,ne,ne,ne,se,s,se,ne,se,ne,ne,ne,se,se,ne,ne,se,ne,ne,ne,ne,se,ne,ne,se,se,n,se,ne,ne,se,ne,sw,se,s,sw,ne,se,se,se,ne,se,ne,ne,ne,s,sw,se,se,ne,sw,ne,se,se,se,ne,ne,se,s,se,se,ne,ne,n,n,ne,ne,ne,ne,ne,ne,se,se,sw,ne,se,ne,ne,se,n,n,se,ne,se,se,nw,ne,se,ne,ne,se,ne,se,sw,sw,ne,ne,se,se,ne,nw,ne,se,se,se,n,se,se,ne,se,ne,se,ne,ne,sw,se,se,n,se,ne,se,se,nw,ne,se,se,ne,se,ne,sw,se,ne,ne,nw,se,se,s,ne,se,ne,ne,ne,se,ne,ne,se,se,ne,ne,se,se,nw,s,se,ne,ne,se,se,se,ne,se,ne,ne,ne,ne,n,ne,se,se,n,se,se,se,se,se,sw,se,se,se,se,se,ne,s,ne,se,ne,ne,se,se,se,se,nw,se,se,ne,ne,s,ne,ne,ne,sw,ne,se,se,se,nw,se,ne,se,ne,se,n,se,ne,se,se,ne,se,ne,nw,se,se,se,ne,ne,nw,ne,ne,se,se,se,ne,sw,se,ne,se,se,ne,ne,se,se,ne,se,ne,se,ne,se,se,ne,se,nw,ne,ne,se,se,ne,ne,ne,nw,sw,ne,ne,ne,ne,se,ne,se,ne,ne,n,se,n,n,se,se,ne,ne,se,sw,n,se,ne,se,ne,ne,se,se,se,se,se,se,ne,se,se,se,n,se,se,sw,se,s,se,se,ne,se,se,se,ne,sw,se,ne,ne,n,n,se,se,ne,ne,s,n,ne,nw,se,se,ne,se,se,se,ne,se,ne,ne,ne,ne,nw,se,se,se,se,se,se,ne,se,ne,se,ne,ne,ne,se,se,se,ne,se,se,se,ne,se,ne,se,se,nw,se,se,se,s,se,se,se,se,se,se,ne,se,se,se,ne,sw,sw,s,ne,se,ne,nw,ne,ne,se,ne,se,ne,se,se,se,ne,se,se,ne,sw,se,sw,ne,se,nw,se,sw,se,ne,se,se,ne,ne,se,se,nw,se,sw,s,se,ne,s,se,se,ne,se,ne,ne,se,se,ne,sw,ne,ne,ne,se,se,se,se,ne,ne,ne,se,n,se,se,se,se,nw,se,ne,n,se,ne,s,ne,n,se,se,se,se,ne,n,ne,ne,se,ne,se,se,ne,se,ne,n,se,se,n,se,se,n,se,ne,s,se,ne,ne,ne,ne,ne,ne,ne,se,se,se,se,se,se,se,se,ne,se,se,se,se,se,se,se,n,se,se,se,se,se,se,ne,se,se,se,s,n,se,se,se,se,se,se,ne,se,ne,se,se,se,s,se,se,se,s,ne,sw,s,se,n,s,sw,se,se,se,ne,n,se,se,ne,se,se,se,se,se,se,se,se,sw,ne,nw,se,sw,se,se,se,nw,se,ne,se,se,se,se,se,se,se,se,se,ne,se,ne,n,se,se,se,ne,n,se,se,se,se,se,se,se,se,ne,se,se,ne,se,se,n,se,nw,se,s,se,ne,n,ne,s,se,se,n,se,se,se,se,ne,se,ne,s,ne,se,se,se,nw,se,se,se,ne,se,se,s,ne,sw,se,sw,ne,nw,se,nw,n,se,se,se,se,ne,se,nw,se,ne,se,se,s,se,ne,se,ne,se,se,se,ne,ne,sw,se,se,se,se,se,se,se,se,se,nw,sw,se,ne,se,se,se,se,se,se,se,ne,s,se,se,se,se,se,se,n,se,n,se,se,se,ne,se,se,se,se,se,se,se,se,se,se,se,se,ne,ne,ne,s,se,se,ne,se,se,n,n,ne,nw,se,se,se,ne,se,sw,se,se,ne,se,se,sw,se,se,se,sw,sw,ne,se,s,s,se,se,se,sw,sw,nw,sw,se,se,ne,se,se,se,se,nw,se,se,se,sw,ne,sw,se,ne,se,se,sw,se,se,se,se,ne,n,sw,se,se,se,se,se,se,se,se,n,se,se,se,se,ne,n,se,se,ne,se,se,nw,se,nw,ne,se,se,se,se,n,se,n,se,se,se,se,se,sw,nw,se,se,sw,se,se,se,se,n,se,n,se,n,se,se,se,se,se,se,se,se,se,se,se,nw,se,nw,n,se,se,se,s,se,sw,se,se,se,se,ne,sw,nw,se,nw,se,se,ne,n,n,nw,nw,sw,s,sw,n,sw,sw,sw,sw,s,se,s,s,sw,nw,sw,s,s,s,s,s,se,s,se,s,se,se,se,se,sw,se,se,ne,se,se,se,se,se,se,se,se,s,ne,ne,n,ne,s,sw,s,ne,s,ne,se,sw,ne,ne,s,ne,ne,n,ne,ne,ne,n,ne,ne,ne,ne,sw,se,n,ne,ne,n,n,ne,ne,ne,ne,n,n,n,ne,ne,n,n,n,ne,s,n,n,n,n,n,n,n,n,ne,n,nw,n,n,s,n,n,n,sw,n,sw,n,n,n,n,nw,sw,se,nw,n,nw,nw,n,n,nw,nw,nw,n,nw,nw,nw,nw,n,n,nw,nw,nw,nw,n,nw,nw,nw,n,nw,nw,nw,n,sw,nw,nw,nw,nw,sw,nw,nw,nw,nw,nw,sw,nw,nw,nw,sw,nw,nw,n,nw,sw,nw,sw,nw,nw,s,s,s,sw,nw,sw,nw,n,nw,sw,nw,sw,se,se,nw,sw,nw,s,sw,sw,sw,nw,s,ne,sw,sw,s,sw,s,sw,se,nw,sw,sw,sw,nw,sw,nw,sw,sw,ne,sw,n,sw,sw,sw,sw,sw,sw,sw,sw,sw,sw,sw,s,s,sw,sw,ne,sw,sw,sw,s,sw,sw,s,sw,sw,sw,sw,sw,sw,n,s,sw,nw,sw,sw,s,sw,s,sw,sw,sw,sw,sw,s,sw,s,s,se,s,s,s,s,s,sw,s,nw,sw,s,sw,s,ne,se,nw,sw,s,ne,s,s,sw,n,se,s,s,s,s,s,s,s,s,s,s,nw,s,s,s,s,s,s,s,sw,s,n,s,sw,ne,s,s,s,sw,s,s,s,s,s,ne,n,n,s,ne,s,s,nw,s,s,s,s,ne,s,s,s,s,nw,n,s,s,s,s,s,se,se,ne,n,s,s,s,se,s,s,s,se,se,ne,s,n,se,se,s,s,s,sw,s,s,s,s,sw,s,s,s,s,s,s,se,sw,se,s,s,s,se,s,s,s,sw,se,s,s,s,se,s,se,n,se,se,se,s,nw,se,se,n,nw,se,se,se,s,se,n,s,s,s,se,se,s,se,n,ne,se,se,se,se,se,se,se,n,nw,se,s,n,se,se,se,se,se,se,s,s,s,se,se,se,se,nw,s,se,se,nw,se,n,se,se,s,nw,se,se,se,nw,se,se,se,ne,se,nw,se,se,se,se,se,se,se,se,se,se,se,ne,se,n,se,se,se,se,se,se,se,sw,se,se,se,sw,nw,se,se,se,se,ne,se,ne,nw,ne,se,ne,se,se,se,se,se,se,se,s,s,se,se,se,sw,n,se,se,ne,ne,se,se,nw,nw,se,se,se,s,s,se,s,se,se,se,ne,se,se,ne,se,se,se,se,nw,ne,se,ne,ne,ne,se,se,ne,n,se,n,se,ne,se,se,ne,se,se,ne,se,n,ne,ne,ne,ne,se,ne,ne,se,se,s,ne,se,se,n,se,ne,ne,se,ne,se,se,se,se,ne,se,se,se,ne,ne,ne,ne,s,ne,se,ne,ne,n,se,ne,ne,n,se,ne,ne,se,ne,ne,ne,ne,ne,se,se,ne,n,ne,ne,ne,se,nw,sw,ne,ne,se,ne,sw,se,ne,ne,ne,ne,ne,ne,s,n,ne,ne,ne,ne,ne,n,ne,ne,ne,s,ne,nw,ne,ne,sw,ne,ne,ne,sw,n,ne,sw,sw,s,ne,ne,ne,ne,s,n,ne,ne,ne,ne,ne,ne,ne,ne,ne,ne,ne,ne,ne,ne,ne,ne,ne,sw,s,ne,ne,n,se,sw,ne,ne,ne,ne,ne,ne,n,ne,ne,nw,ne,ne,ne,n,ne,ne,ne,ne,s,ne,n,ne,s,ne,se,ne,ne,s,nw,ne,ne,se,se,n,ne,ne,ne,ne,ne,ne,ne,ne,ne,ne,ne,ne,ne,ne,n,nw,sw,n,n,sw,ne,ne,n,ne,ne,ne,ne,ne,ne,ne,ne,ne,ne,n,ne,ne,ne,ne,se,ne,n,ne,ne,n,ne,n,ne,se,ne,n,n,ne,ne,ne,ne,se,ne,n,ne,ne,n,n,ne,ne,ne,ne,ne,sw,nw,ne,se,n,n,se,n,s,s,n,n,ne,ne,n,ne,n,nw,n,n,ne,nw,n,n,n,n,ne,sw,nw,nw,n,nw,n,n,n,ne,n,sw,ne,ne,n,n,n,ne,ne,ne,ne,n,ne,n,ne,sw,n,n,s,ne,ne,s,n,n,n,n,se,ne,se,ne,n,n,nw,ne,se,ne,n,n,nw,ne,n,ne,n,n,n,n,n,ne,ne,nw,sw,nw,ne,n,n,n,ne,ne,n,nw,se,n,se,n,sw,ne,se,n,ne,ne,sw,n,n,ne,n,n,n,s,nw,n,n,ne,s,ne,n,s,n,n,n,n,n,n,ne,n,n,n,ne,se,n,n,sw,se,s,n,se,s,n,s,ne,n,n,se,ne,n,n,ne,nw,n,n,ne,n,n,n,n,n,nw,n,ne,sw,ne,ne,n,n,s,n,nw,se,n,n,sw,se,n,n,n,n,nw,n,nw,n,sw,n,n,n,n,ne,n,n,n,ne,nw,n,n,n,ne,ne,n,n,n,nw,n,n,n,n,n,sw,n,n,n,n,n,n,n,nw,s,n,n,n,s,nw,nw,s,n,nw,nw,nw,n,ne,n,n,n,nw,n,nw,n,n,sw,n,n,s,nw,n,nw,nw,n,nw,n,n,n,n,n,n,n,s,n,s,n,n,n,n,sw,n,n,sw,n,nw,n,n,nw,nw,nw,n,s,n,n,n,nw,se,n,n,nw,n,nw,n,n,nw,n,s,s,s,n,n,nw,nw,n,n,n,n,n,nw,n,nw,nw,nw,n,nw,nw,nw,sw,nw,n,n,ne,n,nw,n,n,n,s,s,se,sw,nw,nw,n,sw,n,se,n,n,n,n,n,n,nw,n,sw,nw,nw,s,n,n,s,n,n,n,n,nw,nw,nw,nw,nw,ne,n,n,s,ne,nw,n,nw,n,nw,n,n,n,nw,nw,n,se,n,s,n,s,n,n,se,n,sw,nw,n,n,nw,nw,n,nw,nw,nw,n,n,nw,nw,nw,nw,nw,nw,nw,ne,n,nw,nw,n,nw,n,nw,nw,n,nw,nw,nw,n,nw,n,s,nw,n,nw,ne,nw,n,s,n,nw,nw,n,nw,nw,s,ne,nw,nw,nw,n,nw,nw,nw,n,nw,n,nw,nw,s,ne,se,nw,nw,nw,nw,s,nw,ne,n,n,nw,n,n,ne,n,n,nw,s,nw,s,n,nw,nw,nw,se,nw,se,nw,s,n,n,n,n,nw,nw,sw,se,n,nw,sw,sw,nw,nw,nw,sw,ne,nw,nw,nw,se,nw,n,nw,n,ne,s,nw,n,ne,nw,nw,sw,nw,nw,nw,nw,nw,nw,ne,nw,n,nw,n,sw,s,n,nw,nw,n,n,nw,nw,nw,ne,nw,nw,nw,nw,n,n,nw,ne,nw,nw,nw,ne,s,n,nw,nw,nw,n,nw,nw,nw,sw,nw,nw,sw,sw,nw,s,nw,nw,se,nw,ne,ne,nw,nw,nw,nw,nw,se,nw,nw,ne,nw,n,nw,nw,nw,sw,nw,nw,nw,nw,s,nw,s,sw,nw,nw,nw,nw,se,nw,nw,se,nw,nw,nw,nw,s,nw,s,nw,nw,nw,nw,nw,nw,nw,nw,sw,nw,nw,nw,ne,sw,nw,n,nw,s,nw,nw,s,nw,s,nw,sw,nw,nw,sw,ne,nw,nw,nw,nw,n,nw,nw,nw,nw,nw,nw,nw,nw,se,sw,s,nw,sw,nw,s,nw,s,nw,nw,nw,nw,nw,se,n,s,nw,nw,se,s,s,nw,nw,nw,s,nw,nw,n,s,nw,ne,sw,nw,n,se,nw,nw,nw,nw,ne,nw,nw,sw,nw,n,nw,nw,sw,nw,nw,sw,nw,nw,nw,nw,nw,sw,nw,ne,se,nw,sw,sw,nw,nw,nw,nw,nw,sw,nw,n,nw,nw,nw,nw,n,nw,sw,nw,se,s,se,nw,nw,nw,nw,nw,nw,nw,ne,nw,nw,nw,nw,nw,sw,nw,nw,nw,sw,n,nw,se,nw,nw,nw,sw,nw,nw,nw,nw,sw,se,nw,n,nw,sw,nw,sw,ne,nw,n,nw,sw,nw,sw,nw,nw,sw,ne,s,sw,s,nw,n,nw,nw,nw,nw,sw,sw,sw,nw,nw,nw,sw,nw,nw,nw,sw,nw,nw,nw,nw,sw,nw,nw,nw,s,se,nw,n,sw,nw,nw,nw,nw,sw,sw,s,se,ne,nw,se,s,sw,sw,sw,nw,nw,nw,nw,sw,n,sw,s,se,nw,sw,sw,nw,sw,n,sw,sw,nw,nw,sw,sw,n,n,nw,sw,ne,nw,n,ne,sw,sw,nw,sw,sw,sw,nw,nw,nw,nw,nw,se,nw,nw,nw,sw,sw,s,nw,ne,sw,nw,nw,nw,nw,sw,nw,s,sw,nw,nw,sw,sw,se,nw,nw,nw,sw,nw,s,se,sw,n,se,sw,nw,nw,s,nw,nw,sw,nw,sw,n,nw,se,se,sw,sw,sw,nw,sw,nw,nw,sw,sw,sw,sw,n,sw,s,sw,nw,sw,sw,sw,nw,sw,sw,sw,sw,sw,nw,sw,nw,sw,sw,sw,nw,sw,sw,sw,nw,nw,sw,s,sw,nw,sw,n,sw,nw,sw,sw,nw,sw,sw,ne,sw,sw,n,sw,n,nw,s,s,sw,nw,nw,nw,sw,sw,n,ne,sw,sw,se,sw,sw,sw,sw,sw,sw,nw,s,se,nw,sw,sw,sw,nw,sw,nw,sw,sw,sw,ne,sw,ne,sw,sw,sw,ne,sw,sw,sw,sw,sw,nw,sw,nw,sw,nw,sw,sw,nw,sw,sw,ne,sw,nw,sw,s,sw,sw,sw,sw,sw,sw,sw,sw,n,sw,sw,ne,sw,ne,ne,nw,sw,sw,sw,s,nw,sw,sw,sw,s,sw,sw,sw,sw,sw,se,sw,se,sw,sw,sw,nw,sw,n,sw,s,sw,sw,sw,se,sw,sw,sw,sw,sw,nw,n,sw,sw,sw,sw,ne,sw,sw,sw,nw,sw,sw,n,s,sw,s,sw,sw,sw,sw,sw,se,sw,sw,se,nw,n,sw,sw,sw,sw,sw,sw,sw,s,sw,nw,sw,sw,sw,ne,sw,nw,sw,sw,sw,sw,sw,sw,sw,ne,sw,s,sw,sw,sw,s,ne,sw,ne,sw,n,sw,sw,sw,sw,n,sw,sw,sw,sw,sw,se,sw,sw,sw,sw,sw,nw,sw,nw,sw,nw,sw,sw,sw,sw,s,se,sw,sw,n,sw,n,sw,sw,sw,sw,sw,sw,sw,sw,sw,sw,sw,sw,sw,sw,sw,sw,sw,s,nw,sw,sw,ne,sw,ne,sw,sw,sw,sw,sw,sw,sw,sw,sw,sw,nw,sw,sw,sw,sw,s,sw,sw,sw,sw,sw,s,sw,s,sw,sw,sw,sw,sw,sw,s,sw,se,sw,sw,sw,nw,sw,sw,se,ne,sw,ne,sw,ne,n,nw,ne,sw,sw,sw,sw,sw,sw,sw,s,nw,sw,sw,sw,sw,sw,ne,s,sw,sw,sw,sw,sw,sw,sw,sw,n,sw,se,sw,s,sw,sw,sw,sw,sw,sw,sw,sw,sw,s,sw,sw,ne,sw,sw,s,sw,sw,sw,sw,sw,sw,ne,ne,sw,sw,sw,s,sw,s,sw,sw,s,sw,sw,sw,n,sw,s,n,n,sw,sw,s,sw,sw,ne,nw,s,sw,sw,sw,sw,sw,sw,sw,s,sw,sw,sw,sw,sw,sw,sw,sw,sw,s,sw,s,se,ne,sw,sw,s,sw,sw,sw,s,sw,sw,nw,sw,s,sw,sw,s,s,sw,sw,sw,sw,sw,sw,se,sw,ne,ne,sw,nw,ne,sw,n,sw,sw,sw,n,sw,s,s,se,nw,sw,sw,sw,n,sw,sw,s,sw,s,sw,se,sw,nw,s,sw,s,sw,sw,sw,sw,s,ne,sw,sw,sw,sw,ne,n,s,ne,sw,s,s,sw,sw,ne,sw,sw,nw,s,sw,s,s,sw,sw,sw,se,sw,sw,s,sw,sw,s,s,sw,s,ne,sw,sw,ne,s,nw,sw,s,sw,sw,s,sw,sw,sw,s,s,sw,se,sw,sw,s,sw,sw,s,sw,sw,s,sw,se,sw,sw,s,sw,s,sw,se,ne,sw,s,s,s,s,s,sw,sw,sw,sw,sw,sw,s,sw,n,s,sw,s,n,s,sw,ne,sw,s,s,sw,sw,sw,sw,sw,sw,ne,sw,se,s,sw,nw,s,sw,s,sw,s,se,sw,sw,s,se,s,ne,sw,s,sw,sw,sw,sw,nw,s,s,s,sw,sw,nw,sw,n,sw,s,s,sw,s,sw,sw,s,sw,sw,s,sw,s,nw,sw,sw,sw,sw,s,s,sw,s,sw,s,sw,se,sw,nw,s,s,sw,nw,sw,s,sw,sw,sw,sw,se,ne,s,sw,nw,s,sw,s,s,sw,ne,sw,s,s,s,sw,nw,s,ne,s,s,s,se,sw,sw,s,s,s,sw,s,sw,sw,sw,se,s,sw,s,s,s,se,sw,s,s,sw,s,sw,s,se,s,sw,s,se,sw,s,s,sw,sw,s,nw,sw,s,sw,s,s,s,s,sw,sw,sw,s,s,se,nw,s,s,sw,s,s,sw,sw,s,s,s,sw,se,s,ne,s,s,sw,s,s,s,sw,sw,s,s,sw,sw,s,s,sw,sw,sw,s,sw,s,sw,s,s,s,s,ne,sw,s,s,s,sw,n,sw,s,s,s,s,sw,s,s,sw,s,ne,s,s,s,se,s,n,sw,nw,s,sw,s,s,sw,sw,nw,sw,ne,s,sw,sw,s,s,s,s,sw,s,s,s,s,s,n,s,nw,sw,s,s,s,sw,sw,n,sw,sw,sw,s,s,se,s,s,s,sw,sw,s,ne,s,s,s,se,s,s,s,sw,nw,s,n,sw,sw,s,n,sw,s,s,sw,sw,s,s,s,n,s,s,sw,s,s,s,sw,s,s,ne,s,s,sw,s,sw,s,s,s,s,s,s,s,sw,sw,s,s,s,s,s,s,sw,s,s,s,s,s,sw,s,s,sw,s,nw,s,sw,s,s,s,s,s,s,s,s,s,s,n,sw,sw,s,s,s,sw,s,s,s,s,s,s,s,s,s,n,s,s,n,s,s,s,s,s,s,s,s,s,s,s,sw,s,s,s,s,s,sw,s,s,s,s,s,nw,s,s,nw,s,nw,sw,s,s,s,s,s,s,s,s,s,s,s,s,s,s,s,s,s,s,s,s,s,s,s,s,s,nw,s,s,nw,s,s,s,se,s,s,s,s,s,se,s,s,s,s,s,s,s,s,s,s,s,s,s,s,s,sw,s,s,s,nw,n,s,s,s,s,s,ne,s,s,n,s,s"""
directions = {'n':(2,0), 'ne':(1,1), 'se':(-1,1), 's':(-2,0), 'sw':(-1, -1), 'nw':(1, -1)}
pref = [(-1,-1), (1,-1),(1,1), (-1,1)]
other = [(-2,0),(2,0)]
def move_out(dirs):
    location = [0,0]
    for ins in dirs.split(','):
        change = directions[ins]
#         print('{} -> {} {}'.format(location, ins, change))
        location[0] += change[0]
        location[1] += change[1]
    return location
def find_steps_back(location):
    steps = 0
    while location != [0,0]:
        x, y = location
        flag = False
        for pre in pref:
            dx, dy = pre
            if flag:
                break
            if abs(x+dx) < abs(x) and abs(y+dy) < abs(y):
#                 print('{} ->{}-> {}'.format(location, pre, (dx+x, dy+y)))
                location = [x+dx, y+dy]
                steps += 1
                flag = True
        for ot in other:
            if flag:
                break
            dx, dy = ot
            if abs(x+dx) <= abs(x) and abs(y+dy) <= abs(y):
#                 print('{} ->{}-> {}'.format(location, ot, (dx+x, dy+y)))
                location = [x+dx, y+dy]
                steps += 1
                flag = True
        flag = False
    return steps
def solve(directions):
    loc = move_out(directions)
    steps = find_steps_back(loc)
    return steps
    
# print(solve(data))
assert solve('ne,ne,ne') == 3
assert solve('ne,ne,sw,sw') == 0
assert solve('ne,ne,s,s') == 2
assert solve('se,sw,se,sw,sw') == 3
def move_out(dirs):
    location = [0,0]
    furtest = 0
    for ins in dirs.split(','):
        change = directions[ins]
#         print('{} -> {} {}'.format(location, ins, change))
        location[0] += change[0]
        location[1] += change[1]
        new_steps = find_steps_back(location)
        furtest = max(furtest, new_steps)
    return furtest
memory = {(0,0):0}
def find_steps_back(location):
    in_loc = location
    steps = 0
    while location != [0,0]:
        if tuple(location) in memory:
#             print('{} found in memory steps: {}'.format(location, memory[tuple(location)]))
            return steps+memory[tuple(location)]
        x, y = location
        flag = False
        for pre in pref:
            dx, dy = pre
            if flag:
                break
            if abs(x+dx) < abs(x) and abs(y+dy) < abs(y):
#                 print('{} ->{}-> {}'.format(location, pre, (dx+x, dy+y)))
                location = [x+dx, y+dy]
                steps += 1
                flag = True
        for ot in other:
            if flag:
                break
            dx, dy = ot
            if abs(x+dx) == 0 and abs(y+dy) > 0:
                continue
            if abs(x+dx) <= abs(x) and abs(y+dy) <= abs(y):
#                 print('{} ->{}-> {}'.format(location, ot, (dx+x, dy+y)))
                location = [x+dx, y+dy]
                steps += 1
                flag = True
        if not flag:
            for pre in pref:
                dx, dy = pre
                if abs(y + dy) < abs(y):
#                     print('{} ->{}-> {}'.format(location, pre, (dx+x, dy+y)))
                    location = [x+dx, y+dy]
                    steps += 1
    memory[tuple(in_loc)] = steps
    return steps
def solve(directions):
    return move_out(directions)
# assert solve('ne,ne,ne') == 3
# assert solve('ne,ne,sw,sw') == 2
# assert solve('ne,ne,s,s') == 2
# assert solve('se,sw,se,sw,sw') == 4
d = '''se,s,ne,sw,sw,sw,sw,sw,ne,sw,nw,nw,nw,nw,ne,n,nw,nw,n,sw,n,n,n,n,n,ne,nw,ne,n,sw,n,ne,ne,ne,ne,sw,ne,nw,n,ne,ne,ne,sw,ne,ne,s,se,ne,se,se,se,s,se,se,se,se,se,se,se,se,ne,se,se,ne,se,s,s,se,se,se,s,se,s,s,se,s,s,s,s,se,ne,se,se,s,s,sw,s,s,n,sw,s,s,s,s,s,s,s,s,s,s,s,s,s,sw,s,s,s,s,s,n,s,nw,s,s,s,s,s,se,s,sw,se,sw,s,sw,sw,nw,s,s,se,s,s,s,sw,s,se,sw,sw,sw,sw,ne,s,sw,sw,s,sw,nw,sw,sw,sw,sw,s,sw,sw,sw,se,sw,sw,sw,s,sw,n,sw,sw,s,nw,sw,sw,ne,n,se,sw,sw,sw,nw,sw,n,nw,sw,nw,se,sw,sw,nw,sw,n,sw,sw,nw,sw,sw,nw,n,nw,nw,nw,n,n,nw,sw,n,nw,se,nw,nw,nw,n,sw,nw,nw,nw,ne,sw,nw,s,nw,nw,nw,nw,nw,nw,nw,nw,ne,n,nw,nw,nw,se,nw,n,nw,nw,se,nw,nw,nw,nw,nw,nw,nw,nw,nw,nw,nw,nw,nw,se,nw,nw,n,s,se,s,s,s,n,n,n,ne,nw,n,s,n,n,nw,nw,n,n,nw,nw,n,n,n,nw,n,n,n,nw,n,n,nw,n,n,n,nw,nw,n,se,n,nw,n,s,nw,se,se,nw,nw,n,n,nw,n,nw,nw,nw,nw,n,n,nw,n,ne,n,n,n,n,n,n,n,n,n,n,n,n,s,n,se,n,n,ne,se,n,n,n,ne,n'''
print(solve(data))
data = ['0 <-> 889, 1229, 1736', '1 <-> 1, 480, 793, 1361', '2 <-> 607', '3 <-> 273, 422', '4 <-> 965, 1052, 1130, 1591', '5 <-> 1998', '6 <-> 483, 1628', '7 <-> 1012, 1242, 1244, 1491', '8 <-> 524', '9 <-> 13, 281, 1498', '10 <-> 10', '11 <-> 1956', '12 <-> 598, 621, 1210', '13 <-> 9', '14 <-> 1728', '15 <-> 912, 1461', '16 <-> 1489, 1680, 1994', '17 <-> 854', '18 <-> 1157, 1299', '19 <-> 759', '20 <-> 1352, 1831', '21 <-> 1425', '22 <-> 470, 685, 857, 1526', '23 <-> 405', '24 <-> 43, 536, 1849', '25 <-> 1674', '26 <-> 26, 1738', '27 <-> 558', '28 <-> 1863', '29 <-> 154, 649, 1818', '30 <-> 721, 1366', '31 <-> 725', '32 <-> 413, 880, 903', '33 <-> 414, 442, 1403', '34 <-> 489, 1308', '35 <-> 385, 1254, 1464', '36 <-> 167, 1013, 1860', '37 <-> 535', '38 <-> 605, 1297', '39 <-> 680, 1408, 1982', '40 <-> 169, 615, 952, 1547', '41 <-> 644, 991, 1319, 1509', '42 <-> 453, 1315', '43 <-> 24, 200, 805', '44 <-> 919, 1083', '45 <-> 500', '46 <-> 1532, 1550', '47 <-> 910, 1837', '48 <-> 1849', '49 <-> 542, 1945', '50 <-> 57, 660', '51 <-> 354, 934', '52 <-> 1212', '53 <-> 569', '54 <-> 706', '55 <-> 55, 114, 1077', '56 <-> 1453', '57 <-> 50, 1438', '58 <-> 616, 738', '59 <-> 1242', '60 <-> 312, 523, 648', '61 <-> 748, 1780, 1965', '62 <-> 1533, 1909', '63 <-> 562, 661, 1016', '64 <-> 280, 300, 677', '65 <-> 661, 698, 1881', '66 <-> 283, 440', '67 <-> 382, 421', '68 <-> 986, 1592, 1824', '69 <-> 541, 1363', '70 <-> 266, 1855', '71 <-> 371, 433, 1055, 1682', '72 <-> 793', '73 <-> 73', '74 <-> 1139', '75 <-> 770, 1190, 1409, 1433, 1886', '76 <-> 1135', '77 <-> 492, 1771', '78 <-> 575, 1107, 1596, 1670', '79 <-> 1374', '80 <-> 1168, 1519', '81 <-> 1258', '82 <-> 919, 1519, 1768', '83 <-> 1463', '84 <-> 684', '85 <-> 517, 1655', '86 <-> 1226', '87 <-> 1700', '88 <-> 523, 1292, 1939', '89 <-> 177, 1695, 1706', '90 <-> 400, 1683', '91 <-> 194', '92 <-> 106, 1546', '93 <-> 104', '94 <-> 501, 1686', '95 <-> 285, 1985', '96 <-> 402, 770', '97 <-> 196', '98 <-> 318, 1827', '99 <-> 220, 1272, 1766, 1802', '100 <-> 1105', '101 <-> 380, 957', '102 <-> 1305, 1483', '103 <-> 262, 481, 621', '104 <-> 93, 708, 1731', '105 <-> 282', '106 <-> 92, 901', '107 <-> 553, 742, 1833', '108 <-> 480, 1140', '109 <-> 1247', '110 <-> 1549', '111 <-> 1283', '112 <-> 1503, 1963', '113 <-> 819, 1601', '114 <-> 55, 593, 1020', '115 <-> 324', '116 <-> 378', '117 <-> 1534', '118 <-> 1740, 1836', '119 <-> 1223, 1283', '120 <-> 435, 1063', '121 <-> 404, 939', '122 <-> 294, 360, 1809', '123 <-> 1166', '124 <-> 1988', '125 <-> 163', '126 <-> 126', '127 <-> 255, 754', '128 <-> 634, 969', '129 <-> 563, 1732, 1926', '130 <-> 1196', '131 <-> 1019, 1429', '132 <-> 1287, 1417', '133 <-> 1453', '134 <-> 184, 786', '135 <-> 647', '136 <-> 260, 306', '137 <-> 1342', '138 <-> 292', '139 <-> 1265', '140 <-> 613', '141 <-> 1001, 1217', '142 <-> 142, 1901', '143 <-> 758, 822, 1533', '144 <-> 866, 930, 1197, 1443, 1665', '145 <-> 1672', '146 <-> 1937', '147 <-> 1409, 1697', '148 <-> 608, 954, 1624', '149 <-> 527, 652, 1938', '150 <-> 709', '151 <-> 447, 1305, 1314', '152 <-> 1741', '153 <-> 901, 1997', '154 <-> 29, 929', '155 <-> 1178, 1976', '156 <-> 560', '157 <-> 522', '158 <-> 541', '159 <-> 1212, 1878', '160 <-> 1078', '161 <-> 1128, 1913', '162 <-> 588, 734', '163 <-> 125, 1073, 1952', '164 <-> 1156', '165 <-> 1781', '166 <-> 1692', '167 <-> 36, 1637', '168 <-> 1043, 1085', '169 <-> 40, 334, 1257, 1313', '170 <-> 170', '171 <-> 171', '172 <-> 1391', '173 <-> 925', '174 <-> 1733', '175 <-> 175, 1466', '176 <-> 726, 1182', '177 <-> 89, 1100', '178 <-> 611, 1141', '179 <-> 1036, 1307', '180 <-> 1556', '181 <-> 1930', '182 <-> 775, 1284', '183 <-> 1907', '184 <-> 134, 1981', '185 <-> 255, 1278', '186 <-> 1891', '187 <-> 531, 1318', '188 <-> 790, 1623', '189 <-> 379, 1749, 1865', '190 <-> 1103, 1676', '191 <-> 534', '192 <-> 477', '193 <-> 193, 860', '194 <-> 91, 710, 1780', '195 <-> 290, 1383, 1510', '196 <-> 97, 1664', '197 <-> 1416', '198 <-> 287, 1760', '199 <-> 366', '200 <-> 43', '201 <-> 813, 1882', '202 <-> 246, 1175', '203 <-> 203, 1007', '204 <-> 204, 923', '205 <-> 924', '206 <-> 1162, 1818', '207 <-> 365, 487, 923', '208 <-> 1281, 1290', '209 <-> 1280', '210 <-> 210, 288, 1333', '211 <-> 211, 417, 754', '212 <-> 1698', '213 <-> 1626', '214 <-> 1256', '215 <-> 215, 1385, 1671', '216 <-> 811, 1025', '217 <-> 554, 1715', '218 <-> 1483', '219 <-> 1741', '220 <-> 99, 530, 1081, 1319, 1801', '221 <-> 804, 1144', '222 <-> 1288, 1702', '223 <-> 223, 1231', '224 <-> 649, 1179', '225 <-> 1271, 1776', '226 <-> 226, 1991', '227 <-> 496, 857, 1004, 1821', '228 <-> 371, 500', '229 <-> 1162', '230 <-> 693, 1081', '231 <-> 506, 973', '232 <-> 859, 969, 1922', '233 <-> 233', '234 <-> 875, 1006', '235 <-> 1035, 1998', '236 <-> 236', '237 <-> 289, 569, 1440', '238 <-> 1249, 1923', '239 <-> 1564, 1775, 1944', '240 <-> 1888', '241 <-> 951, 1874', '242 <-> 825', '243 <-> 384, 983, 1838', '244 <-> 715, 1501', '245 <-> 592, 671', '246 <-> 202, 391, 632, 656', '247 <-> 663', '248 <-> 253, 752', '249 <-> 1073, 1558', '250 <-> 290', '251 <-> 792, 1389', '252 <-> 797', '253 <-> 248, 771', '254 <-> 254, 1047', '255 <-> 127, 185, 369', '256 <-> 623', '257 <-> 1636, 1740', '258 <-> 317', '259 <-> 1775', '260 <-> 136, 561, 1290', '261 <-> 359, 1657', '262 <-> 103, 697, 1074', '263 <-> 1205', '264 <-> 1779, 1782', '265 <-> 1407', '266 <-> 70, 1215, 1306', '267 <-> 333, 790', '268 <-> 603', '269 <-> 269, 1497', '270 <-> 270, 1613', '271 <-> 1416, 1562, 1923', '272 <-> 579, 894', '273 <-> 3, 993', '274 <-> 333', '275 <-> 1188', '276 <-> 535, 645, 1166, 1269', '277 <-> 1369', '278 <-> 744, 1717', '279 <-> 349, 695, 985, 1096', '280 <-> 64, 1516', '281 <-> 9, 427, 768, 1468', '282 <-> 105, 867', '283 <-> 66, 1235, 1525, 1748', '284 <-> 530', '285 <-> 95, 800, 1191', '286 <-> 339, 611, 1581', '287 <-> 198, 1285, 1501', '288 <-> 210, 1059', '289 <-> 237, 1928', '290 <-> 195, 250, 1934', '291 <-> 337, 1902', '292 <-> 138, 1805, 1849', '293 <-> 906', '294 <-> 122, 1582', '295 <-> 602', '296 <-> 778', '297 <-> 471, 483', '298 <-> 298', '299 <-> 402, 729', '300 <-> 64, 1002', '301 <-> 856', '302 <-> 1084, 1538, 1739', '303 <-> 892, 1774', '304 <-> 1029, 1350', '305 <-> 521, 1628, 1902', '306 <-> 136, 469, 653, 835', '307 <-> 981', '308 <-> 1997', '309 <-> 1612', '310 <-> 1338, 1571', '311 <-> 1388', '312 <-> 60', '313 <-> 1557', '314 <-> 886, 1704', '315 <-> 672, 779', '316 <-> 1062, 1906', '317 <-> 258, 1290', '318 <-> 98, 318', '319 <-> 1974', '320 <-> 839', '321 <-> 395, 615, 909, 1046', '322 <-> 1077, 1390, 1989', '323 <-> 323, 773, 1571', '324 <-> 115, 493, 511, 650', '325 <-> 325', '326 <-> 1944, 1972', '327 <-> 1489', '328 <-> 412, 468', '329 <-> 1637', '330 <-> 556, 1176', '331 <-> 656', '332 <-> 564, 1688', '333 <-> 267, 274, 421, 1205, 1743', '334 <-> 169, 1896', '335 <-> 1176', '336 <-> 638, 1408, 1633', '337 <-> 291, 844, 1549', '338 <-> 515', '339 <-> 286', '340 <-> 340, 1959', '341 <-> 943', '342 <-> 417, 638, 1116, 1536', '343 <-> 1030', '344 <-> 584, 1751', '345 <-> 345, 1810', '346 <-> 346', '347 <-> 587', '348 <-> 515, 1187', '349 <-> 279, 349', '350 <-> 1749', '351 <-> 1030, 1097', '352 <-> 352', '353 <-> 353, 683', '354 <-> 51, 354, 735', '355 <-> 1362', '356 <-> 1593', '357 <-> 357', '358 <-> 441, 501, 899, 1672', '359 <-> 261', '360 <-> 122, 360, 1234, 1927', '361 <-> 736', '362 <-> 1169', '363 <-> 780', '364 <-> 444, 905, 1049, 1911', '365 <-> 207', '366 <-> 199, 1469', '367 <-> 1612', '368 <-> 675, 1800', '369 <-> 255', '370 <-> 370, 873, 962, 1238', '371 <-> 71, 228, 456', '372 <-> 1912', '373 <-> 1318', '374 <-> 1018, 1246', '375 <-> 898, 1303', '376 <-> 376, 573', '377 <-> 1080', '378 <-> 116, 1140', '379 <-> 189, 1984', '380 <-> 101', '381 <-> 472, 827, 1097', '382 <-> 67', '383 <-> 383, 582', '384 <-> 243, 432, 444, 569, 634', '385 <-> 35', '386 <-> 1496', '387 <-> 637, 737, 756, 1293', '388 <-> 1562', '389 <-> 633', '390 <-> 488', '391 <-> 246, 853, 1422', '392 <-> 1253, 1331', '393 <-> 921, 1567, 1777, 1970', '394 <-> 809', '395 <-> 321, 798, 1040', '396 <-> 746, 1332', '397 <-> 400, 953', '398 <-> 1958', '399 <-> 399', '400 <-> 90, 397, 808, 1485', '401 <-> 1395', '402 <-> 96, 299, 1388', '403 <-> 716', '404 <-> 121', '405 <-> 23, 934, 1221', '406 <-> 1007', '407 <-> 1391', '408 <-> 497, 1090, 1644', '409 <-> 1479', '410 <-> 793, 1977', '411 <-> 1026', '412 <-> 328, 581, 806', '413 <-> 32, 1354', '414 <-> 33, 1920', '415 <-> 799, 1207, 1880', '416 <-> 1862', '417 <-> 211, 342, 589, 1858', '418 <-> 556, 1437, 1490', '419 <-> 1393', '420 <-> 420', '421 <-> 67, 333, 1813', '422 <-> 3, 706, 1598, 1721', '423 <-> 1834', '424 <-> 854, 1442', '425 <-> 855, 1080', '426 <-> 1408, 1469', '427 <-> 281', '428 <-> 832, 1998', '429 <-> 553, 657, 834', '430 <-> 1466', '431 <-> 1357', '432 <-> 384', '433 <-> 71', '434 <-> 434, 489, 1137', '435 <-> 120', '436 <-> 972, 1461', '437 <-> 550', '438 <-> 486, 844', '439 <-> 978', '440 <-> 66, 705, 1850', '441 <-> 358, 589, 783, 804, 1129', '442 <-> 33, 497', '443 <-> 1806', '444 <-> 364, 384, 1698', '445 <-> 1208, 1294, 1452', '446 <-> 1143, 1452', '447 <-> 151, 1072', '448 <-> 448', '449 <-> 997, 1829', '450 <-> 1277', '451 <-> 1531, 1866', '452 <-> 1175, 1622, 1975', '453 <-> 42, 1486', '454 <-> 689', '455 <-> 1497', '456 <-> 371, 1577', '457 <-> 702', '458 <-> 461, 921, 1279', '459 <-> 1004', '460 <-> 485, 505, 1211, 1451', '461 <-> 458, 541, 916, 1844', '462 <-> 1281', '463 <-> 856, 1481', '464 <-> 602, 1476, 1553', '465 <-> 543, 1566', '466 <-> 847, 1593', '467 <-> 1270', '468 <-> 328, 829', '469 <-> 306, 667, 720, 1931', '470 <-> 22', '471 <-> 297', '472 <-> 381', '473 <-> 473', '474 <-> 599, 1146', '475 <-> 1570, 1894', '476 <-> 1145', '477 <-> 192, 1193, 1690', '478 <-> 1469, 1840', '479 <-> 1684', '480 <-> 1, 108', '481 <-> 103, 963', '482 <-> 1778', '483 <-> 6, 297, 1662', '484 <-> 1435', '485 <-> 460', '486 <-> 438', '487 <-> 207, 998, 1185', '488 <-> 390, 1231, 1668', '489 <-> 34, 434, 1341', '490 <-> 990, 1203', '491 <-> 936', '492 <-> 77', '493 <-> 324', '494 <-> 1984', '495 <-> 495, 1954', '496 <-> 227', '497 <-> 408, 442, 1551', '498 <-> 1704, 1788', '499 <-> 836', '500 <-> 45, 228, 1358, 1798', '501 <-> 94, 358, 1559', '502 <-> 951', '503 <-> 1036', '504 <-> 1303', '505 <-> 460', '506 <-> 231, 606, 1473', '507 <-> 1109', '508 <-> 1724', '509 <-> 1644', '510 <-> 848', '511 <-> 324, 1036', '512 <-> 523', '513 <-> 809, 1294', '514 <-> 785', '515 <-> 338, 348, 1027, 1193, 1226', '516 <-> 1988', '517 <-> 85, 1482', '518 <-> 518', '519 <-> 1625', '520 <-> 520', '521 <-> 305, 1033', '522 <-> 157, 1355, 1476, 1588', '523 <-> 60, 88, 512', '524 <-> 8, 1998', '525 <-> 990, 1275', '526 <-> 1310, 1552', '527 <-> 149, 979, 1805', '528 <-> 698', '529 <-> 631, 970', '530 <-> 220, 284, 1533, 1944', '531 <-> 187, 551, 1168, 1574', '532 <-> 1484', '533 <-> 892', '534 <-> 191, 879', '535 <-> 37, 276, 1527', '536 <-> 24, 1094', '537 <-> 747, 952', '538 <-> 1620, 1735', '539 <-> 858, 1467', '540 <-> 1263, 1572', '541 <-> 69, 158, 461', '542 <-> 49, 1384', '543 <-> 465, 639, 873', '544 <-> 1338', '545 <-> 1967', '546 <-> 806, 1239', '547 <-> 792, 1039, 1078', '548 <-> 548, 1891, 1941', '549 <-> 861', '550 <-> 437, 1209, 1967', '551 <-> 531, 888, 896', '552 <-> 798', '553 <-> 107, 429, 1330, 1951', '554 <-> 217', '555 <-> 744, 947, 1246', '556 <-> 330, 418, 1070, 1925', '557 <-> 1826, 1854', '558 <-> 27, 1629', '559 <-> 1042, 1150', '560 <-> 156, 1472, 1834', '561 <-> 260', '562 <-> 63', '563 <-> 129, 1309', '564 <-> 332', '565 <-> 1770, 1842', '566 <-> 621', '567 <-> 1160, 1178, 1642', '568 <-> 895', '569 <-> 53, 237, 384', '570 <-> 641', '571 <-> 571, 1261, 1924', '572 <-> 882', '573 <-> 376', '574 <-> 982', '575 <-> 78, 1255', '576 <-> 887, 1539', '577 <-> 603, 1122, 1679', '578 <-> 742', '579 <-> 272, 1444, 1747', '580 <-> 797, 1554, 1718', '581 <-> 412, 1926', '582 <-> 383', '583 <-> 1611', '584 <-> 344, 1620', '585 <-> 1692', '586 <-> 1383', '587 <-> 347, 1351', '588 <-> 162, 1220', '589 <-> 417, 441', '590 <-> 1919', '591 <-> 884, 992', '592 <-> 245, 814', '593 <-> 114', '594 <-> 1843', '595 <-> 1809', '596 <-> 837', '597 <-> 1563, 1575', '598 <-> 12, 605, 984', '599 <-> 474, 1218', '600 <-> 732, 1237, 1714', '601 <-> 1913', '602 <-> 295, 464, 1061', '603 <-> 268, 577, 720', '604 <-> 604', '605 <-> 38, 598', '606 <-> 506, 686, 1813', '607 <-> 2, 1948', '608 <-> 148', '609 <-> 1571', '610 <-> 772, 901', '611 <-> 178, 286, 880', '612 <-> 1814', '613 <-> 140, 883, 1198, 1764, 1942', '614 <-> 1352', '615 <-> 40, 321', '616 <-> 58, 1413', '617 <-> 624, 1008, 1591, 1791', '618 <-> 1625', '619 <-> 871, 1567', '620 <-> 1954', '621 <-> 12, 103, 566', '622 <-> 1895', '623 <-> 256, 1767', '624 <-> 617', '625 <-> 663', '626 <-> 626', '627 <-> 1650', '628 <-> 884', '629 <-> 1104, 1421', '630 <-> 630, 864', '631 <-> 529, 646', '632 <-> 246', '633 <-> 389, 1847', '634 <-> 128, 384', '635 <-> 1553, 1817', '636 <-> 636', '637 <-> 387', '638 <-> 336, 342, 646, 1453', '639 <-> 543, 815, 1087', '640 <-> 1422, 1597', '641 <-> 570, 805, 993, 1961', '642 <-> 1371', '643 <-> 959, 1044, 1444', '644 <-> 41', '645 <-> 276, 1022, 1184', '646 <-> 631, 638, 1790', '647 <-> 135, 1286', '648 <-> 60', '649 <-> 29, 224, 1636', '650 <-> 324', '651 <-> 863, 1321', '652 <-> 149, 687, 1128, 1346', '653 <-> 306', '654 <-> 1409', '655 <-> 1142, 1733', '656 <-> 246, 331, 768, 1815', '657 <-> 429', '658 <-> 1511, 1569', '659 <-> 1744', '660 <-> 50, 796, 1524', '661 <-> 63, 65, 810', '662 <-> 995, 1661', '663 <-> 247, 625, 1001', '664 <-> 664', '665 <-> 1305', '666 <-> 666, 1817', '667 <-> 469, 1003, 1550', '668 <-> 1540, 1958', '669 <-> 831, 883, 1349, 1719', '670 <-> 1531', '671 <-> 245, 671, 1693', '672 <-> 315, 1088', '673 <-> 942, 1381, 1660', '674 <-> 880', '675 <-> 368', '676 <-> 1269, 1699', '677 <-> 64, 1654', '678 <-> 784', '679 <-> 1760', '680 <-> 39', '681 <-> 681', '682 <-> 728, 749, 1995', '683 <-> 353', '684 <-> 84, 1150', '685 <-> 22', '686 <-> 606', '687 <-> 652, 1687', '688 <-> 1878', '689 <-> 454, 689', '690 <-> 924, 1183', '691 <-> 1410, 1413', '692 <-> 1702', '693 <-> 230, 1658', '694 <-> 820, 1282, 1873', '695 <-> 279', '696 <-> 1168', '697 <-> 262, 766, 776', '698 <-> 65, 528, 698, 940', '699 <-> 1778', '700 <-> 743, 1459, 1825', '701 <-> 1475', '702 <-> 457, 792, 861, 1467', '703 <-> 1581', '704 <-> 1969', '705 <-> 440, 1145', '706 <-> 54, 422', '707 <-> 1015, 1780', '708 <-> 104, 1266', '709 <-> 150, 1778', '710 <-> 194', '711 <-> 751', '712 <-> 963', '713 <-> 1525, 1762', '714 <-> 1713', '715 <-> 244, 1293, 1421', '716 <-> 403, 1572', '717 <-> 1142', '718 <-> 1204', '719 <-> 1672', '720 <-> 469, 603', '721 <-> 30, 1268, 1400', '722 <-> 1183', '723 <-> 1012', '724 <-> 1029, 1289, 1368', '725 <-> 31, 1039', '726 <-> 176, 726', '727 <-> 856', '728 <-> 682, 1000', '729 <-> 299, 1216, 1967', '730 <-> 850, 900', '731 <-> 1540, 1884', '732 <-> 600, 784', '733 <-> 1655', '734 <-> 162', '735 <-> 354, 1955', '736 <-> 361, 1084, 1822', '737 <-> 387', '738 <-> 58, 1573', '739 <-> 1119, 1216, 1822', '740 <-> 829, 1219', '741 <-> 1164', '742 <-> 107, 578', '743 <-> 700, 1744', '744 <-> 278, 555', '745 <-> 835, 1903', '746 <-> 396', '747 <-> 537, 1843', '748 <-> 61', '749 <-> 682, 1217, 1731', '750 <-> 874, 1110, 1724', '751 <-> 711, 1767', '752 <-> 248, 1011', '753 <-> 1327, 1885', '754 <-> 127, 211, 1117', '755 <-> 755', '756 <-> 387', '757 <-> 1098, 1169', '758 <-> 143, 1689', '759 <-> 19, 1517', '760 <-> 831, 1915', '761 <-> 761, 1195', '762 <-> 1634', '763 <-> 763', '764 <-> 848, 1375', '765 <-> 765, 1136', '766 <-> 697, 1295, 1887', '767 <-> 1906', '768 <-> 281, 656, 1031', '769 <-> 1457, 1863', '770 <-> 75, 96', '771 <-> 253, 846, 1375', '772 <-> 610', '773 <-> 323', '774 <-> 1067', '775 <-> 182, 1494', '776 <-> 697', '777 <-> 1136', '778 <-> 296, 1057', '779 <-> 315, 1631, 1796', '780 <-> 363, 780, 1814', '781 <-> 928, 1423', '782 <-> 1850', '783 <-> 441', '784 <-> 678, 732, 999, 1988', '785 <-> 514, 1248', '786 <-> 134, 786, 1009', '787 <-> 1348, 1863', '788 <-> 891, 1183, 1455', '789 <-> 1310, 1420, 1510', '790 <-> 188, 267', '791 <-> 1276', '792 <-> 251, 547, 702', '793 <-> 1, 72, 410, 1092', '794 <-> 880', '795 <-> 1799, 1807', '796 <-> 660, 1548', '797 <-> 252, 580, 797', '798 <-> 395, 552', '799 <-> 415, 799', '800 <-> 285, 1889', '801 <-> 801', '802 <-> 802', '803 <-> 1188, 1326, 1935', '804 <-> 221, 441', '805 <-> 43, 641, 1772', '806 <-> 412, 546, 918, 1617', '807 <-> 876, 1887', '808 <-> 400, 1435, 1716', '809 <-> 394, 513', '810 <-> 661', '811 <-> 216, 1259', '812 <-> 1883', '813 <-> 201, 1692', '814 <-> 592', '815 <-> 639', '816 <-> 1041, 1734', '817 <-> 1134, 1432', '818 <-> 1575', '819 <-> 113, 1063', '820 <-> 694', '821 <-> 1242', '822 <-> 143, 892', '823 <-> 1393, 1492', '824 <-> 946', '825 <-> 242, 999', '826 <-> 1594', '827 <-> 381, 1079, 1580', '828 <-> 1941', '829 <-> 468, 740, 1905', '830 <-> 977, 1260, 1861', '831 <-> 669, 760, 946, 1332', '832 <-> 428, 832, 944, 1172', '833 <-> 837, 1008, 1470', '834 <-> 429, 915', '835 <-> 306, 745, 976', '836 <-> 499, 967', '837 <-> 596, 833, 974', '838 <-> 1335', '839 <-> 320, 839, 1703', '840 <-> 1053, 1398, 1760', '841 <-> 1193', '842 <-> 842, 1066, 1108', '843 <-> 1414, 1697, 1894', '844 <-> 337, 438', '845 <-> 1506', '846 <-> 771', '847 <-> 466, 907, 1432', '848 <-> 510, 764', '849 <-> 1063, 1195, 1701', '850 <-> 730, 1551', '851 <-> 1112, 1331, 1479', '852 <-> 1652', '853 <-> 391', '854 <-> 17, 424, 906, 1665', '855 <-> 425, 1082', '856 <-> 301, 463, 727, 1744', '857 <-> 22, 227', '858 <-> 539, 1252, 1472', '859 <-> 232, 1843', '860 <-> 193', '861 <-> 549, 702, 1709, 1884', '862 <-> 1149', '863 <-> 651, 955', '864 <-> 630', '865 <-> 1138', '866 <-> 144, 1111, 1114', '867 <-> 282, 1487, 1835', '868 <-> 1699', '869 <-> 869', '870 <-> 1487', '871 <-> 619', '872 <-> 872', '873 <-> 370, 543, 1968', '874 <-> 750, 874', '875 <-> 234, 1202, 1473', '876 <-> 807, 933, 1741', '877 <-> 1205, 1874', '878 <-> 1831', '879 <-> 534, 1860', '880 <-> 32, 611, 674, 794', '881 <-> 1361, 1750', '882 <-> 572, 1495', '883 <-> 613, 669', '884 <-> 591, 628, 1815', '885 <-> 996, 1237', '886 <-> 314, 1709', '887 <-> 576', '888 <-> 551', '889 <-> 0, 1494', '890 <-> 1100, 1966', '891 <-> 788, 1312', '892 <-> 303, 533, 822, 1334, 1812, 1935', '893 <-> 1723', '894 <-> 272, 1992', '895 <-> 568, 1038', '896 <-> 551, 1425', '897 <-> 1783', '898 <-> 375', '899 <-> 358', '900 <-> 730', '901 <-> 106, 153, 610', '902 <-> 1203', '903 <-> 32, 1935', '904 <-> 1109', '905 <-> 364', '906 <-> 293, 854, 1565', '907 <-> 847, 1139, 1180, 1431, 1563, 1878', '908 <-> 1908', '909 <-> 321, 943', '910 <-> 47, 1067', '911 <-> 1468, 1495', '912 <-> 15', '913 <-> 1692', '914 <-> 922, 1445', '915 <-> 834, 1002', '916 <-> 461', '917 <-> 1177, 1924', '918 <-> 806, 962, 1058, 1419', '919 <-> 44, 82, 1933', '920 <-> 1147, 1539', '921 <-> 393, 458, 1055, 1951', '922 <-> 914, 1271', '923 <-> 204, 207, 1201', '924 <-> 205, 690', '925 <-> 173, 1816', '926 <-> 1279', '927 <-> 927', '928 <-> 781', '929 <-> 154', '930 <-> 144', '931 <-> 972, 1237', '932 <-> 1317', '933 <-> 876, 1756', '934 <-> 51, 405, 1105, 1960', '935 <-> 935, 1674', '936 <-> 491, 1201, 1247', '937 <-> 956, 1576, 1788', '938 <-> 1377, 1733', '939 <-> 121, 1638', '940 <-> 698, 1808', '941 <-> 1665, 1957', '942 <-> 673', '943 <-> 341, 909', '944 <-> 832', '945 <-> 1087, 1340', '946 <-> 824, 831', '947 <-> 555', '948 <-> 959', '949 <-> 1068', '950 <-> 1664', '951 <-> 241, 502, 1151', '952 <-> 40, 537, 1376', '953 <-> 397', '954 <-> 148, 1075, 1364', '955 <-> 863, 1235, 1618, 1724', '956 <-> 937', '957 <-> 101, 1323', '958 <-> 1794, 1972', '959 <-> 643, 948, 1023', '960 <-> 960, 1417', '961 <-> 1278', '962 <-> 370, 918', '963 <-> 481, 712', '964 <-> 1198', '965 <-> 4', '966 <-> 966', '967 <-> 836, 967, 1821', '968 <-> 1513', '969 <-> 128, 232', '970 <-> 529', '971 <-> 1471', '972 <-> 436, 931', '973 <-> 231', '974 <-> 837', '975 <-> 1390', '976 <-> 835', '977 <-> 830', '978 <-> 439, 1687', '979 <-> 527', '980 <-> 980, 1609, 1940', '981 <-> 307, 1671', '982 <-> 574, 1318, 1643', '983 <-> 243', '984 <-> 598', '985 <-> 279', '986 <-> 68', '987 <-> 1060', '988 <-> 1942', '989 <-> 1478', '990 <-> 490, 525, 1838', '991 <-> 41, 1263, 1302', '992 <-> 591', '993 <-> 273, 641', '994 <-> 1026, 1240, 1618', '995 <-> 662, 1545', '996 <-> 885, 1528', '997 <-> 449, 1058', '998 <-> 487', '999 <-> 784, 825', '1000 <-> 728', '1001 <-> 141, 663, 1626, 1681', '1002 <-> 300, 915', '1003 <-> 667', '1004 <-> 227, 459', '1005 <-> 1780', '1006 <-> 234, 1578', '1007 <-> 203, 406', '1008 <-> 617, 833', '1009 <-> 786, 1064', '1010 <-> 1010, 1031, 1919', '1011 <-> 752, 1754', '1012 <-> 7, 723, 1068, 1181', '1013 <-> 36', '1014 <-> 1594', '1015 <-> 707', '1016 <-> 63', '1017 <-> 1511', '1018 <-> 374, 1034', '1019 <-> 131, 1155', '1020 <-> 114', '1021 <-> 1288', '1022 <-> 645', '1023 <-> 959, 1375', '1024 <-> 1024', '1025 <-> 216', '1026 <-> 411, 994', '1027 <-> 515', '1028 <-> 1417', '1029 <-> 304, 724', '1030 <-> 343, 351', '1031 <-> 768, 1010', '1032 <-> 1032', '1033 <-> 521', '1034 <-> 1018', '1035 <-> 235, 1578', '1036 <-> 179, 503, 511, 1036', '1037 <-> 1037, 1044', '1038 <-> 895, 1125', '1039 <-> 547, 725, 1599', '1040 <-> 395', '1041 <-> 816', '1042 <-> 559, 1042', '1043 <-> 168, 1873', '1044 <-> 643, 1037, 1312', '1045 <-> 1232', '1046 <-> 321', '1047 <-> 254', '1048 <-> 1747', '1049 <-> 364', '1050 <-> 1050, 1947, 1963', '1051 <-> 1156', '1052 <-> 4, 1201', '1053 <-> 840', '1054 <-> 1133, 1342, 1537, 1708, 1778', '1055 <-> 71, 921, 1786', '1056 <-> 1672', '1057 <-> 778, 1423, 1787', '1058 <-> 918, 997', '1059 <-> 288, 1337, 1401', '1060 <-> 987, 1781', '1061 <-> 602, 1660', '1062 <-> 316, 1863', '1063 <-> 120, 819, 849', '1064 <-> 1009', '1065 <-> 1065', '1066 <-> 842', '1067 <-> 774, 910, 1089', '1068 <-> 949, 1012', '1069 <-> 1900', '1070 <-> 556', '1071 <-> 1884', '1072 <-> 447, 1122', '1073 <-> 163, 249, 1073, 1237', '1074 <-> 262', '1075 <-> 954, 1075, 1789', '1076 <-> 1076, 1680', '1077 <-> 55, 322', '1078 <-> 160, 547', '1079 <-> 827, 1079', '1080 <-> 377, 425, 1739', '1081 <-> 220, 230', '1082 <-> 855, 1638', '1083 <-> 44', '1084 <-> 302, 736', '1085 <-> 168, 1431', '1086 <-> 1973', '1087 <-> 639, 945', '1088 <-> 672', '1089 <-> 1067, 1190', '1090 <-> 408, 1492', '1091 <-> 1674', '1092 <-> 793', '1093 <-> 1802', '1094 <-> 536', '1095 <-> 1095, 1204', '1096 <-> 279', '1097 <-> 351, 381', '1098 <-> 757, 1519', '1099 <-> 1099, 1752', '1100 <-> 177, 890', '1101 <-> 1145', '1102 <-> 1280', '1103 <-> 190, 1200', '1104 <-> 629', '1105 <-> 100, 934', '1106 <-> 1426', '1107 <-> 78, 1497', '1108 <-> 842', '1109 <-> 507, 904, 1109', '1110 <-> 750', '1111 <-> 866', '1112 <-> 851', '1113 <-> 1113', '1114 <-> 866, 1131, 1861', '1115 <-> 1187, 1629', '1116 <-> 342', '1117 <-> 754', '1118 <-> 1637', '1119 <-> 739', '1120 <-> 1837', '1121 <-> 1133, 1758', '1122 <-> 577, 1072, 1349', '1123 <-> 1359', '1124 <-> 1174', '1125 <-> 1038, 1789', '1126 <-> 1260', '1127 <-> 1213', '1128 <-> 161, 652', '1129 <-> 441', '1130 <-> 4', '1131 <-> 1114', '1132 <-> 1132, 1979', '1133 <-> 1054, 1121, 1253', '1134 <-> 817', '1135 <-> 76, 1606', '1136 <-> 765, 777, 1860', '1137 <-> 434', '1138 <-> 865, 1280, 1471, 1736', '1139 <-> 74, 907', '1140 <-> 108, 378', '1141 <-> 178', '1142 <-> 655, 717', '1143 <-> 446', '1144 <-> 221', '1145 <-> 476, 705, 1101, 1271, 1956', '1146 <-> 474, 1179, 1936', '1147 <-> 920, 1147', '1148 <-> 1148, 1795', '1149 <-> 862, 1799', '1150 <-> 559, 684, 1797', '1151 <-> 951', '1152 <-> 1229', '1153 <-> 1515, 1530', '1154 <-> 1154', '1155 <-> 1019, 1300', '1156 <-> 164, 1051, 1156', '1157 <-> 18, 1157', '1158 <-> 1208', '1159 <-> 1651', '1160 <-> 567, 1510, 1710', '1161 <-> 1161, 1427, 1590', '1162 <-> 206, 229, 1561', '1163 <-> 1388', '1164 <-> 741, 1494', '1165 <-> 1217', '1166 <-> 123, 276', '1167 <-> 1262, 1547', '1168 <-> 80, 531, 696', '1169 <-> 362, 757, 1504', '1170 <-> 1854', '1171 <-> 1171, 1898', '1172 <-> 832', '1173 <-> 1173, 1315', '1174 <-> 1124, 1174, 1831', '1175 <-> 202, 452', '1176 <-> 330, 335, 1761', '1177 <-> 917', '1178 <-> 155, 567', '1179 <-> 224, 1146', '1180 <-> 907, 1661', '1181 <-> 1012', '1182 <-> 176', '1183 <-> 690, 722, 788', '1184 <-> 645', '1185 <-> 487', '1186 <-> 1659', '1187 <-> 348, 1115, 1670', '1188 <-> 275, 803', '1189 <-> 1689', '1190 <-> 75, 1089', '1191 <-> 285', '1192 <-> 1744', '1193 <-> 477, 515, 841', '1194 <-> 1308', '1195 <-> 761, 849', '1196 <-> 130, 1993', '1197 <-> 144', '1198 <-> 613, 964, 1329', '1199 <-> 1389', '1200 <-> 1103', '1201 <-> 923, 936, 1052', '1202 <-> 875', '1203 <-> 490, 902, 1692', '1204 <-> 718, 1095, 1245', '1205 <-> 263, 333, 877', '1206 <-> 1311', '1207 <-> 415, 1883', '1208 <-> 445, 1158', '1209 <-> 550, 1640', '1210 <-> 12, 1210, 1428', '1211 <-> 460, 1529', '1212 <-> 52, 159, 1493, 1819', '1213 <-> 1127, 1213', '1214 <-> 1214, 1436', '1215 <-> 266, 1758', '1216 <-> 729, 739', '1217 <-> 141, 749, 1165, 1315', '1218 <-> 599, 1595', '1219 <-> 740, 1549', '1220 <-> 588, 1374', '1221 <-> 405', '1222 <-> 1966', '1223 <-> 119', '1224 <-> 1528', '1225 <-> 1314', '1226 <-> 86, 515', '1227 <-> 1681', '1228 <-> 1228', '1229 <-> 0, 1152, 1374', '1230 <-> 1453', '1231 <-> 223, 488', '1232 <-> 1045, 1261', '1233 <-> 1759', '1234 <-> 360', '1235 <-> 283, 955, 1241, 1783', '1236 <-> 1356', '1237 <-> 600, 885, 931, 1073', '1238 <-> 370, 1602', '1239 <-> 546, 1373', '1240 <-> 994', '1241 <-> 1235, 1392', '1242 <-> 7, 59, 821, 1945', '1243 <-> 1296', '1244 <-> 7, 1300, 1434', '1245 <-> 1204, 1347', '1246 <-> 374, 555, 1508', '1247 <-> 109, 936', '1248 <-> 785, 1715', '1249 <-> 238', '1250 <-> 1600, 1623', '1251 <-> 1251', '1252 <-> 858', '1253 <-> 392, 1133', '1254 <-> 35, 1394', '1255 <-> 575', '1256 <-> 214, 1607, 1685', '1257 <-> 169', '1258 <-> 81, 1264, 1320', '1259 <-> 811, 1425', '1260 <-> 830, 1126', '1261 <-> 571, 1232', '1262 <-> 1167, 1862', '1263 <-> 540, 991', '1264 <-> 1258, 1651', '1265 <-> 139, 1569', '1266 <-> 708', '1267 <-> 1267', '1268 <-> 721', '1269 <-> 276, 676, 1759', '1270 <-> 467, 1270, 1916', '1271 <-> 225, 922, 1145, 1700', '1272 <-> 99', '1273 <-> 1302', '1274 <-> 1966', '1275 <-> 525', '1276 <-> 791, 1834', '1277 <-> 450, 1474, 1645', '1278 <-> 185, 961', '1279 <-> 458, 926', '1280 <-> 209, 1102, 1138', '1281 <-> 208, 462, 1943', '1282 <-> 694, 1522', '1283 <-> 111, 119, 1407', '1284 <-> 182, 1996', '1285 <-> 287', '1286 <-> 647, 1286, 1715', '1287 <-> 132', '1288 <-> 222, 1021, 1398', '1289 <-> 724', '1290 <-> 208, 260, 317', '1291 <-> 1498', '1292 <-> 88', '1293 <-> 387, 715, 1322, 1519, 1645', '1294 <-> 445, 513, 1504', '1295 <-> 766', '1296 <-> 1243, 1379, 1964', '1297 <-> 38, 1669', '1298 <-> 1906', '1299 <-> 18, 1804', '1300 <-> 1155, 1244', '1301 <-> 1371, 1453', '1302 <-> 991, 1273', '1303 <-> 375, 504, 1948', '1304 <-> 1667, 1933', '1305 <-> 102, 151, 665', '1306 <-> 266', '1307 <-> 179', '1308 <-> 34, 1194', '1309 <-> 563', '1310 <-> 526, 789', '1311 <-> 1206, 1311, 1769', '1312 <-> 891, 1044', '1313 <-> 169', '1314 <-> 151, 1225', '1315 <-> 42, 1173, 1217', '1316 <-> 1316', '1317 <-> 932, 1805', '1318 <-> 187, 373, 982', '1319 <-> 41, 220, 1948', '1320 <-> 1258, 1859', '1321 <-> 651', '1322 <-> 1293', '1323 <-> 957, 1472', '1324 <-> 1324', '1325 <-> 1325', '1326 <-> 803, 1846', '1327 <-> 753', '1328 <-> 1879', '1329 <-> 1198', '1330 <-> 553, 1330', '1331 <-> 392, 851', '1332 <-> 396, 831', '1333 <-> 210', '1334 <-> 892', '1335 <-> 838, 1552, 1568', '1336 <-> 1336', '1337 <-> 1059', '1338 <-> 310, 544', '1339 <-> 1897', '1340 <-> 945', '1341 <-> 489', '1342 <-> 137, 1054', '1343 <-> 1343', '1344 <-> 1946', '1345 <-> 1345', '1346 <-> 652', '1347 <-> 1245, 1914, 1930', '1348 <-> 787, 1591', '1349 <-> 669, 1122', '1350 <-> 304, 1790', '1351 <-> 587, 1997', '1352 <-> 20, 614', '1353 <-> 1738', '1354 <-> 413, 1608', '1355 <-> 522, 1816, 1917', '1356 <-> 1236, 1450', '1357 <-> 431, 1575', '1358 <-> 500', '1359 <-> 1123, 1599', '1360 <-> 1370, 1385', '1361 <-> 1, 881', '1362 <-> 355, 1611, 1952', '1363 <-> 69', '1364 <-> 954', '1365 <-> 1948', '1366 <-> 30, 1470', '1367 <-> 1527', '1368 <-> 724', '1369 <-> 277, 1482', '1370 <-> 1360', '1371 <-> 642, 1301, 1478, 1485', '1372 <-> 1372, 1594', '1373 <-> 1239', '1374 <-> 79, 1220, 1229', '1375 <-> 764, 771, 1023', '1376 <-> 952', '1377 <-> 938, 1520, 1730', '1378 <-> 1378, 1411, 1823', '1379 <-> 1296, 1832', '1380 <-> 1380', '1381 <-> 673', '1382 <-> 1382', '1383 <-> 195, 586', '1384 <-> 542', '1385 <-> 215, 1360', '1386 <-> 1386', '1387 <-> 1536', '1388 <-> 311, 402, 1163', '1389 <-> 251, 1199', '1390 <-> 322, 975', '1391 <-> 172, 407, 1453', '1392 <-> 1241, 1587', '1393 <-> 419, 823, 1636', '1394 <-> 1254, 1588, 1699', '1395 <-> 401, 1621', '1396 <-> 1396, 1870', '1397 <-> 1629', '1398 <-> 840, 1288', '1399 <-> 1399, 1932', '1400 <-> 721', '1401 <-> 1059', '1402 <-> 1402', '1403 <-> 33', '1404 <-> 1449, 1632, 1832', '1405 <-> 1634', '1406 <-> 1726', '1407 <-> 265, 1283, 1999', '1408 <-> 39, 336, 426', '1409 <-> 75, 147, 654', '1410 <-> 691, 1780', '1411 <-> 1378', '1412 <-> 1447, 1759', '1413 <-> 616, 691', '1414 <-> 843', '1415 <-> 1415', '1416 <-> 197, 271', '1417 <-> 132, 960, 1028', '1418 <-> 1418, 1426', '1419 <-> 918, 1560', '1420 <-> 789', '1421 <-> 629, 715', '1422 <-> 391, 640', '1423 <-> 781, 1057', '1424 <-> 1614', '1425 <-> 21, 896, 1259', '1426 <-> 1106, 1418', '1427 <-> 1161', '1428 <-> 1210, 1677', '1429 <-> 131', '1430 <-> 1822', '1431 <-> 907, 1085, 1846', '1432 <-> 817, 847', '1433 <-> 75', '1434 <-> 1244', '1435 <-> 484, 808', '1436 <-> 1214', '1437 <-> 418', '1438 <-> 57', '1439 <-> 1469, 1824', '1440 <-> 237', '1441 <-> 1722', '1442 <-> 424, 1678', '1443 <-> 144', '1444 <-> 579, 643, 1869', '1445 <-> 914', '1446 <-> 1524, 1728', '1447 <-> 1412, 1962', '1448 <-> 1485', '1449 <-> 1404', '1450 <-> 1356, 1647', '1451 <-> 460, 1907, 1967', '1452 <-> 445, 446', '1453 <-> 56, 133, 638, 1230, 1301, 1391', '1454 <-> 1994', '1455 <-> 788', '1456 <-> 1914', '1457 <-> 769', '1458 <-> 1458', '1459 <-> 700, 1796', '1460 <-> 1799', '1461 <-> 15, 436', '1462 <-> 1678', '1463 <-> 83, 1553, 1684', '1464 <-> 35', '1465 <-> 1471', '1466 <-> 175, 430', '1467 <-> 539, 702', '1468 <-> 281, 911, 1475', '1469 <-> 366, 426, 478, 1439, 1524', '1470 <-> 833, 1366', '1471 <-> 971, 1138, 1465', '1472 <-> 560, 858, 1323, 1937', '1473 <-> 506, 875', '1474 <-> 1277, 1937', '1475 <-> 701, 1468', '1476 <-> 464, 522', '1477 <-> 1785', '1478 <-> 989, 1371', '1479 <-> 409, 851', '1480 <-> 1677', '1481 <-> 463', '1482 <-> 517, 1369, 1482', '1483 <-> 102, 218', '1484 <-> 532, 1531, 1735', '1485 <-> 400, 1371, 1448', '1486 <-> 453', '1487 <-> 867, 870, 1577, 1584', '1488 <-> 1488', '1489 <-> 16, 327', '1490 <-> 418', '1491 <-> 7, 1589', '1492 <-> 823, 1090', '1493 <-> 1212, 1519, 1675', '1494 <-> 775, 889, 1164', '1495 <-> 882, 911', '1496 <-> 386, 1496', '1497 <-> 269, 455, 1107', '1498 <-> 9, 1291, 1758', '1499 <-> 1685, 1893', '1500 <-> 1657', '1501 <-> 244, 287', '1502 <-> 1951', '1503 <-> 112', '1504 <-> 1169, 1294', '1505 <-> 1987', '1506 <-> 845, 1905', '1507 <-> 1507', '1508 <-> 1246', '1509 <-> 41', '1510 <-> 195, 789, 1160, 1980', '1511 <-> 658, 1017', '1512 <-> 1990', '1513 <-> 968, 1513, 1612', '1514 <-> 1514', '1515 <-> 1153, 1632', '1516 <-> 280', '1517 <-> 759', '1518 <-> 1837', '1519 <-> 80, 82, 1098, 1293, 1493', '1520 <-> 1377, 1978', '1521 <-> 1521', '1522 <-> 1282', '1523 <-> 1749, 1876', '1524 <-> 660, 1446, 1469, 1535, 1729', '1525 <-> 283, 713', '1526 <-> 22, 1767', '1527 <-> 535, 1367, 1889', '1528 <-> 996, 1224', '1529 <-> 1211, 1736', '1530 <-> 1153', '1531 <-> 451, 670, 1484', '1532 <-> 46', '1533 <-> 62, 143, 530', '1534 <-> 117, 1992', '1535 <-> 1524', '1536 <-> 342, 1387', '1537 <-> 1054', '1538 <-> 302, 1589', '1539 <-> 576, 920', '1540 <-> 668, 731', '1541 <-> 1639', '1542 <-> 1542', '1543 <-> 1702', '1544 <-> 1927', '1545 <-> 995', '1546 <-> 92, 1890', '1547 <-> 40, 1167', '1548 <-> 796', '1549 <-> 110, 337, 1219', '1550 <-> 46, 667', '1551 <-> 497, 850', '1552 <-> 526, 1335', '1553 <-> 464, 635, 1463', '1554 <-> 580, 1696', '1555 <-> 1556, 1648, 1867', '1556 <-> 180, 1555, 1676', '1557 <-> 313, 1831', '1558 <-> 249', '1559 <-> 501', '1560 <-> 1419', '1561 <-> 1162', '1562 <-> 271, 388', '1563 <-> 597, 907', '1564 <-> 239', '1565 <-> 906, 1854', '1566 <-> 465', '1567 <-> 393, 619', '1568 <-> 1335, 1745', '1569 <-> 658, 1265, 1651', '1570 <-> 475', '1571 <-> 310, 323, 609', '1572 <-> 540, 716', '1573 <-> 738', '1574 <-> 531', '1575 <-> 597, 818, 1357', '1576 <-> 937', '1577 <-> 456, 1487, 1630', '1578 <-> 1006, 1035', '1579 <-> 1704', '1580 <-> 827', '1581 <-> 286, 703, 1888', '1582 <-> 294', '1583 <-> 1907', '1584 <-> 1487', '1585 <-> 1955', '1586 <-> 1586, 1641', '1587 <-> 1392', '1588 <-> 522, 1394', '1589 <-> 1491, 1538, 1589', '1590 <-> 1161, 1642, 1946', '1591 <-> 4, 617, 1348', '1592 <-> 68', '1593 <-> 356, 466', '1594 <-> 826, 1014, 1372', '1595 <-> 1218', '1596 <-> 78', '1597 <-> 640', '1598 <-> 422', '1599 <-> 1039, 1359', '1600 <-> 1250', '1601 <-> 113, 1631', '1602 <-> 1238', '1603 <-> 1603', '1604 <-> 1604', '1605 <-> 1980', '1606 <-> 1135, 1828', '1607 <-> 1256, 1607', '1608 <-> 1354', '1609 <-> 980, 1864', '1610 <-> 1610', '1611 <-> 583, 1362', '1612 <-> 309, 367, 1513', '1613 <-> 270, 1620', '1614 <-> 1424, 1688', '1615 <-> 1615', '1616 <-> 1884', '1617 <-> 806, 1763', '1618 <-> 955, 994, 1897', '1619 <-> 1622', '1620 <-> 538, 584, 1613', '1621 <-> 1395, 1621', '1622 <-> 452, 1619', '1623 <-> 188, 1250', '1624 <-> 148', '1625 <-> 519, 618, 1625, 1765', '1626 <-> 213, 1001', '1627 <-> 1929', '1628 <-> 6, 305', '1629 <-> 558, 1115, 1397', '1630 <-> 1577', '1631 <-> 779, 1601', '1632 <-> 1404, 1515', '1633 <-> 336', '1634 <-> 762, 1405, 1734', '1635 <-> 1635', '1636 <-> 257, 649, 1393', '1637 <-> 167, 329, 1118', '1638 <-> 939, 1082', '1639 <-> 1541, 1639', '1640 <-> 1209', '1641 <-> 1586', '1642 <-> 567, 1590', '1643 <-> 982', '1644 <-> 408, 509', '1645 <-> 1277, 1293', '1646 <-> 1836, 1875', '1647 <-> 1450, 1772', '1648 <-> 1555, 1946', '1649 <-> 1743', '1650 <-> 627, 1720', '1651 <-> 1159, 1264, 1569', '1652 <-> 852, 1930', '1653 <-> 1653', '1654 <-> 677', '1655 <-> 85, 733', '1656 <-> 1875', '1657 <-> 261, 1500, 1703', '1658 <-> 693, 1679', '1659 <-> 1186, 1659', '1660 <-> 673, 1061', '1661 <-> 662, 1180', '1662 <-> 483', '1663 <-> 1663, 1904', '1664 <-> 196, 950, 1664', '1665 <-> 144, 854, 941', '1666 <-> 1666', '1667 <-> 1304, 1890', '1668 <-> 488', '1669 <-> 1297', '1670 <-> 78, 1187', '1671 <-> 215, 981', '1672 <-> 145, 358, 719, 1056', '1673 <-> 1673', '1674 <-> 25, 935, 1091', '1675 <-> 1493', '1676 <-> 190, 1556', '1677 <-> 1428, 1480', '1678 <-> 1442, 1462, 1987', '1679 <-> 577, 1658', '1680 <-> 16, 1076', '1681 <-> 1001, 1227', '1682 <-> 71', '1683 <-> 90', '1684 <-> 479, 1463, 1852', '1685 <-> 1256, 1499', '1686 <-> 94', '1687 <-> 687, 978, 1787', '1688 <-> 332, 1614, 1688', '1689 <-> 758, 1189, 1779', '1690 <-> 477', '1691 <-> 1691, 1986', '1692 <-> 166, 585, 813, 913, 1203, 1913', '1693 <-> 671', '1694 <-> 1711', '1695 <-> 89, 1795', '1696 <-> 1554', '1697 <-> 147, 843, 1900', '1698 <-> 212, 444, 1793', '1699 <-> 676, 868, 1394, 1705', '1700 <-> 87, 1271', '1701 <-> 849', '1702 <-> 222, 692, 1543', '1703 <-> 839, 1657', '1704 <-> 314, 498, 1579', '1705 <-> 1699', '1706 <-> 89, 1993', '1707 <-> 1990, 1994', '1708 <-> 1054, 1892', '1709 <-> 861, 886', '1710 <-> 1160', '1711 <-> 1694, 1737', '1712 <-> 1712', '1713 <-> 714, 1935', '1714 <-> 600', '1715 <-> 217, 1248, 1286', '1716 <-> 808', '1717 <-> 278, 1914', '1718 <-> 580', '1719 <-> 669', '1720 <-> 1650, 1762, 1856', '1721 <-> 422, 1918', '1722 <-> 1441, 1722', '1723 <-> 893, 1915', '1724 <-> 508, 750, 955', '1725 <-> 1725', '1726 <-> 1406, 1959', '1727 <-> 1797', '1728 <-> 14, 1446', '1729 <-> 1524', '1730 <-> 1377, 1737', '1731 <-> 104, 749', '1732 <-> 129, 1908', '1733 <-> 174, 655, 938', '1734 <-> 816, 1634, 1734', '1735 <-> 538, 1484', '1736 <-> 0, 1138, 1529', '1737 <-> 1711, 1730', '1738 <-> 26, 1353, 1757', '1739 <-> 302, 1080', '1740 <-> 118, 257', '1741 <-> 152, 219, 876', '1742 <-> 1841, 1945', '1743 <-> 333, 1649', '1744 <-> 659, 743, 856, 1192', '1745 <-> 1568', '1746 <-> 1746', '1747 <-> 579, 1048', '1748 <-> 283', '1749 <-> 189, 350, 1523, 1848, 1894', '1750 <-> 881', '1751 <-> 344', '1752 <-> 1099', '1753 <-> 1753', '1754 <-> 1011', '1755 <-> 1755, 1939', '1756 <-> 933', '1757 <-> 1738', '1758 <-> 1121, 1215, 1498', '1759 <-> 1233, 1269, 1412', '1760 <-> 198, 679, 840', '1761 <-> 1176', '1762 <-> 713, 1720', '1763 <-> 1617', '1764 <-> 613', '1765 <-> 1625', '1766 <-> 99', '1767 <-> 623, 751, 1526', '1768 <-> 82', '1769 <-> 1311, 1921', '1770 <-> 565, 1995', '1771 <-> 77, 1771', '1772 <-> 805, 1647, 1772', '1773 <-> 1773, 1826', '1774 <-> 303', '1775 <-> 239, 259', '1776 <-> 225', '1777 <-> 393', '1778 <-> 482, 699, 709, 1054', '1779 <-> 264, 1689', '1780 <-> 61, 194, 707, 1005, 1410, 1999', '1781 <-> 165, 1060, 1978', '1782 <-> 264', '1783 <-> 897, 1235, 1845', '1784 <-> 1784', '1785 <-> 1477, 1915', '1786 <-> 1055', '1787 <-> 1057, 1687, 1899', '1788 <-> 498, 937, 1859', '1789 <-> 1075, 1125', '1790 <-> 646, 1350', '1791 <-> 617', '1792 <-> 1855', '1793 <-> 1698', '1794 <-> 958', '1795 <-> 1148, 1695', '1796 <-> 779, 1459, 1857', '1797 <-> 1150, 1727', '1798 <-> 500', '1799 <-> 795, 1149, 1460', '1800 <-> 368, 1800', '1801 <-> 220', '1802 <-> 99, 1093', '1803 <-> 1810', '1804 <-> 1299', '1805 <-> 292, 527, 1317', '1806 <-> 443, 1865', '1807 <-> 795, 1911', '1808 <-> 940', '1809 <-> 122, 595', '1810 <-> 345, 1803', '1811 <-> 1980', '1812 <-> 892', '1813 <-> 421, 606', '1814 <-> 612, 780', '1815 <-> 656, 884', '1816 <-> 925, 1355', '1817 <-> 635, 666', '1818 <-> 29, 206', '1819 <-> 1212', '1820 <-> 1874', '1821 <-> 227, 967', '1822 <-> 736, 739, 1430', '1823 <-> 1378', '1824 <-> 68, 1439', '1825 <-> 700', '1826 <-> 557, 1773', '1827 <-> 98, 1971', '1828 <-> 1606, 1865', '1829 <-> 449', '1830 <-> 1830', '1831 <-> 20, 878, 1174, 1557', '1832 <-> 1379, 1404, 1832', '1833 <-> 107', '1834 <-> 423, 560, 1276', '1835 <-> 867', '1836 <-> 118, 1646', '1837 <-> 47, 1120, 1518', '1838 <-> 243, 990', '1839 <-> 1839', '1840 <-> 478', '1841 <-> 1742', '1842 <-> 565', '1843 <-> 594, 747, 859', '1844 <-> 461', '1845 <-> 1783', '1846 <-> 1326, 1431', '1847 <-> 633, 1888', '1848 <-> 1749', '1849 <-> 24, 48, 292, 1851', '1850 <-> 440, 782', '1851 <-> 1849', '1852 <-> 1684', '1853 <-> 1853', '1854 <-> 557, 1170, 1565', '1855 <-> 70, 1792', '1856 <-> 1720', '1857 <-> 1796', '1858 <-> 417', '1859 <-> 1320, 1788', '1860 <-> 36, 879, 1136', '1861 <-> 830, 1114', '1862 <-> 416, 1262', '1863 <-> 28, 769, 787, 1062', '1864 <-> 1609, 1920, 1953', '1865 <-> 189, 1806, 1828, 1969', '1866 <-> 451', '1867 <-> 1555', '1868 <-> 1868', '1869 <-> 1444', '1870 <-> 1396', '1871 <-> 1939', '1872 <-> 1914', '1873 <-> 694, 1043', '1874 <-> 241, 877, 1820', '1875 <-> 1646, 1656', '1876 <-> 1523', '1877 <-> 1877', '1878 <-> 159, 688, 907', '1879 <-> 1328, 1879', '1880 <-> 415', '1881 <-> 65', '1882 <-> 201', '1883 <-> 812, 1207', '1884 <-> 731, 861, 1071, 1616', '1885 <-> 753, 1885', '1886 <-> 75', '1887 <-> 766, 807', '1888 <-> 240, 1581, 1847', '1889 <-> 800, 1527', '1890 <-> 1546, 1667', '1891 <-> 186, 548', '1892 <-> 1708', '1893 <-> 1499', '1894 <-> 475, 843, 1749', '1895 <-> 622, 1895, 1978', '1896 <-> 334', '1897 <-> 1339, 1618, 1949', '1898 <-> 1171', '1899 <-> 1787', '1900 <-> 1069, 1697', '1901 <-> 142', '1902 <-> 291, 305', '1903 <-> 745', '1904 <-> 1663', '1905 <-> 829, 1506', '1906 <-> 316, 767, 1298, 1999', '1907 <-> 183, 1451, 1583', '1908 <-> 908, 1732', '1909 <-> 62', '1910 <-> 1999', '1911 <-> 364, 1807', '1912 <-> 372, 1912', '1913 <-> 161, 601, 1692', '1914 <-> 1347, 1456, 1717, 1872', '1915 <-> 760, 1723, 1785', '1916 <-> 1270', '1917 <-> 1355', '1918 <-> 1721', '1919 <-> 590, 1010', '1920 <-> 414, 1864', '1921 <-> 1769', '1922 <-> 232', '1923 <-> 238, 271, 1923', '1924 <-> 571, 917', '1925 <-> 556, 1925', '1926 <-> 129, 581', '1927 <-> 360, 1544', '1928 <-> 289', '1929 <-> 1627, 1929', '1930 <-> 181, 1347, 1652', '1931 <-> 469, 1931', '1932 <-> 1399', '1933 <-> 919, 1304', '1934 <-> 290', '1935 <-> 803, 892, 903, 1713', '1936 <-> 1146', '1937 <-> 146, 1472, 1474', '1938 <-> 149', '1939 <-> 88, 1755, 1871', '1940 <-> 980', '1941 <-> 548, 828', '1942 <-> 613, 988', '1943 <-> 1281', '1944 <-> 239, 326, 530', '1945 <-> 49, 1242, 1742', '1946 <-> 1344, 1590, 1648', '1947 <-> 1050', '1948 <-> 607, 1303, 1319, 1365', '1949 <-> 1897', '1950 <-> 1950', '1951 <-> 553, 921, 1502', '1952 <-> 163, 1362', '1953 <-> 1864', '1954 <-> 495, 620', '1955 <-> 735, 1585', '1956 <-> 11, 1145', '1957 <-> 941', '1958 <-> 398, 668', '1959 <-> 340, 1726', '1960 <-> 934', '1961 <-> 641', '1962 <-> 1447', '1963 <-> 112, 1050', '1964 <-> 1296', '1965 <-> 61', '1966 <-> 890, 1222, 1274', '1967 <-> 545, 550, 729, 1451', '1968 <-> 873', '1969 <-> 704, 1865', '1970 <-> 393', '1971 <-> 1827', '1972 <-> 326, 958', '1973 <-> 1086, 1973', '1974 <-> 319, 1974', '1975 <-> 452', '1976 <-> 155', '1977 <-> 410', '1978 <-> 1520, 1781, 1895', '1979 <-> 1132', '1980 <-> 1510, 1605, 1811', '1981 <-> 184', '1982 <-> 39', '1983 <-> 1983', '1984 <-> 379, 494', '1985 <-> 95', '1986 <-> 1691', '1987 <-> 1505, 1678', '1988 <-> 124, 516, 784', '1989 <-> 322', '1990 <-> 1512, 1707', '1991 <-> 226', '1992 <-> 894, 1534', '1993 <-> 1196, 1706', '1994 <-> 16, 1454, 1707', '1995 <-> 682, 1770', '1996 <-> 1284', '1997 <-> 153, 308, 1351', '1998 <-> 5, 235, 428, 524', '1999 <-> 1407, 1780, 1906, 1910']
from collections import defaultdict
def make_connection_dict(data):
    connections = defaultdict(set)
    for conn in data:
        node, cons = conn.split(' <-> ')
        node = int(node)
        cons = eval('[{}]'.format(cons))
        for con in cons:
            connections[node].add(con)
            connections[con].add(node)
    return connections
def from_zero(start, connections, visited=[], debug=False):
    if debug:
        print(start, connections[start], visited)
    for node in connections[start]:
        if node not in visited:
            visited.append(node)
            from_zero(node, connections, visited, debug)
    return visited
    
def solve(data):
    connections = make_connection_dict(data)
    answer = from_zero(0, connections, debug=False)
    return len(answer)
assert solve(['0 <-> 2', '1 <-> 1', '2 <-> 0, 3, 4', '3 <-> 2, 4', '4 <-> 2, 3, 6', '5 <-> 6', '6 <-> 4, 5']) == 6
print(solve(data))
from collections import defaultdict
def make_connection_dict(data):
    connections = defaultdict(set)
    for conn in data:
        node, cons = conn.split(' <-> ')
        node = int(node)
        cons = eval('[{}]'.format(cons))
        for con in cons:
            connections[node].add(con)
            connections[con].add(node)
    return connections
def find_group(start, connections, visited=[], debug=False):
    if debug:
        print(start, connections[start], visited)
    for node in connections[start]:
        if node not in visited:
            visited.append(node)
            from_zero(node, connections, visited, debug)
    return visited
def solve(data):
    connections = make_connection_dict(data)
    groups = 0
    while len(connections) > 0:
        answer = find_group(list(connections.keys())[0], connections, visited=[], debug=False)
        groups += 1
        for ans in answer:
            del(connections[ans])
    return groups
assert solve(['0 <-> 2', '1 <-> 1', '2 <-> 0, 3, 4', '3 <-> 2, 4', '4 <-> 2, 3, 6', '5 <-> 6', '6 <-> 4, 5']) == 2
print(solve(data))
data = ['0: 3', '1: 2', '2: 4', '4: 6', '6: 4', '8: 6', '10: 5', '12: 6', '14: 8', '16: 8', '18: 8', '20: 6', '22: 12', '24: 8', '26: 8', '28: 10', '30: 9', '32: 12', '34: 8', '36: 12', '38: 12', '40: 12', '42: 14', '44: 14', '46: 12', '48: 12', '50: 12', '52: 12', '54: 14', '56: 12', '58: 14', '60: 14', '62: 14', '64: 14', '70: 10', '72: 14', '74: 14', '76: 14', '78: 14', '82: 14', '86: 17', '88: 18', '96: 26']
def solve(data):
    length = int(data[-1].split(': ')[0])+1
    positions = [None] * length
    for val in data:        
        layer,depth = val.split(': ')
        layer = int(layer)
        depth = int(depth)
#         print(layer,depth)
        positions[layer] = [0, depth, 1]
    cur_pos = -1
    sev = 0
    for x in range(length):
        cur_pos += 1
#         print("moving into: {}".format(cur_pos))
        if positions[cur_pos]:
            if positions[cur_pos][0] == 0:
                sev += cur_pos * positions[cur_pos][1]
#                 print("Encountered sentinal. severity increased with: {} to {}".format(cur_pos * positions[cur_pos][1], sev))
        for pos in positions:
            if not pos:
                continue
            pos[0] = (pos[0]+pos[2])
            if pos[0]==pos[1]-1 or pos[0]==0:
                pos[2] = -1 * pos[2]
#         print(positions)
    return sev
assert solve(['0: 3', '1: 2', '4: 4', '6: 4']) == 24
solve(data)
def solve(data):
    length = int(data[-1].split(': ')[0])+1
    datas = []
    for dat in data:
        a, b = dat.split(': ')
        node = int(a)
        depth = int(b)
        datas.append((node, (depth-1)*2))
#     print(datas)
    pause = 0
    caught = True
    while caught:
        pause += 1
        for node in datas:
            if (pause+node[0])%node[1] == 0:
#                 print("caught at node {} with pause {}".format(node[0], pause))
                break
        else:
            caught=False
    return pause
        
        
assert solve(['0: 3', '1: 2', '4: 4', '6: 4']) == 10
print(solve(data))
def run_once(lengths, data=None, skip=0, pos=0):
    if not data:
        data = list(range(256))
    skip = skip
    pos = pos
    for l in lengths:
        if l == len(data):
            f = (data+data)
            pre = f[:pos]
            rev = f[pos:pos+l][::-1]
            post = f[pos+l:]
            f = pre+rev+post
            data = f[l:l+pos]+f[pos:l]
        elif pos+l > len(data):
            f = (data+data)
            pre = f[:pos]
            rev = f[pos:pos+l][::-1]
            post = f[pos+l:]
            f = pre+rev+post
            data = f[len(data):len(data)+pos] + f[pos:len(data)]        
        else:
            pre = data[:pos]
            rev = data[pos:pos+l]
            post = data[pos+l:]
            data = pre+rev[::-1]+post
        pos = (pos+l+skip)%len(data)
        skip += 1
    return {'data':data, 'skip': skip, 'pos': pos}
def get_lengths(data=''):
    return [ord(x) for x in data]+[17, 31, 73, 47, 23]
    
def run_multiple(lengths=[]):
    rets = {}
    for p in range(64):
        rets = run_once(lengths, **rets)
    return rets['data']
def get_hash(data):
    out = ''
    for x in range(0, len(data), 16):
        tmp=0
        for y in range(16):
            tmp = tmp^data[x+y]
        out += '{:02x}'.format(tmp)
    return out
def knothash(key=None):
    if not key:
        key=''
    lengths = get_lengths(key)
#     print('key: {}\nlengths: {}'.format(key,lengths))
    data = run_multiple(lengths)
#     test_hash = get_hash(data[:16])
#     print('test hash: {}'.format(test_hash))
    return get_hash(data)
data = "nbysizxe"
def get_row(khash):
    row = list("".join(['{:04b}'.format(int(ch,16)) for ch in khash]))
    return row
def solve(data):
    used = 0
    for x in range(128):
        khash = knothash('{}-{}'.format(data, x))
        used += 128-(sorted(get_row(khash)).index('1'))
    return used
    
assert solve('flqrgnkx') == 8108
solve(data)
def get_map(data):
    my_map = []
    for x in range(128):
        khash = knothash('{}-{}'.format(data, x))
        tmp = list(map(int, get_row(khash)))
        my_map.append(tmp)
    return my_map
def get_valid_coords(data, x, y):
    coords = ((1,0), (0,1), (0,-1), (-1,0))
    return ((x+dx, y+dy) for dx, dy in coords if -1 < x+dx < len(data) and -1 < y+dy < len(data[x]))
def remove_island(data, x, y):
    data[x][y] = 0
    for dx, dy in get_valid_coords(data, x, y):
        if data[dx][dy] == 1:
            remove_island(data, dx, dy)
def solve(data):
    islands = 0
    my_map = get_map(data)
    for x in range(len(my_map)):
        for y in range(len(my_map[x])):
            if my_map[x][y] == 1:
                islands +=1
                remove_island(my_map, x, y)
    return islands
                
assert solve('flqrgnkx') == 1242
print(solve(data))