#!/usr/bin/env python
# coding: utf-8
# In[244]:
import numpy as np
import matplotlib.pyplot as plt
import time
import matplotlib.animation as animation
from matplotlib import colors
# In[245]:
def construction_abri(cap , source_inf , vegr , veg , s , jourres , abri):
    """float*bool*int*float*int*bool => bool*int*bool*bool"""
    #sauve:bool
    sauve = False
    #rand:float
    if jourres != 0:
        jourres = jourres - 1
    else:
        abri = True
    if jourres == -11 or vegr == 0:
        jourres = ((45/(cap*0.5)//10 * 1/(veg/5)))/1.
        abri = False
        source_inf = False
        rand = np.random.random_sample()
        if rand < s:
            sauve = True
    jourres = jourres//1
    return jourres , abri , sauve , source_inf
# In[246]:
construction_abri(0.1,False,1,20,0.1,-10,False)
# In[247]:
def trouver_eau(p_eau , capadap , source_inf , hydrat):
    """float*float*bool*float => bool*float"""
    b=0
    if source_inf == 1:
        hydrat = 1
    else:
        rand = np.random.random_sample()
        if rand <= 0.4*p_eau*(2.5*capadap):
            hydrat = hydrat + 0.25
        elif rand <= p_eau*(5*capadap) :
            hydrat = hydrat + 0.5
            rand=np.random.random_sample()
            if rand > 0.4: 
                source_inf = True
    if hydrat > 1:
        hydrat = 1
    return source_inf , hydrat
# In[248]:
def inter_veget(veg,alimentation,capadap,vegre):
   """int*float*float=>int*float"""
   #p_vg:float
   p_vg=0.15
   #trouve:bool
   trouve=True
   #vegr:int
   vegr=vegre
   if vegr == 0:
       vegr = veg
   while vegr>0 and trouve==True:
       rand=np.random.random_sample()
       if rand * (capadap)+0.06 >=p_vg:
           alimentation = alimentation + 0.10*(capadap+0.1)
           vegr = vegr - 1
           p_vg = p_vg+0.08
       else:
           trouve=False
   if alimentation > 1:
       alimentation = 1
   return alimentation , vegr
# In[249]:
def inter_anim(p_a, force, capadap, alimentation, sante,c):
    """
    float ^6 -> float ^2
    hyp : 
    """
 
    random1 = np.random.random_sample()
    if random1 <= p_a : 
        alimentation = alimentation + 0.15
    if alimentation > 1:
        alimentation = 1.0
        
    return alimentation , sante , c
# In[250]:
def sante_fct_hydr_alim(alimentation,hydratation,sante,abri,force,c):
    """float³=>float
    force en fonction de l'alimentation et hydratation"""
    
    if abri==True:
        sante=sante+0.025
    
    if alimentation >= 0.7 and hydratation >=0.7:
        if sante<0.2:
            sante = 0.2
        else:
            sante = sante + 0.05
    elif alimentation>=0.5 and hydratation >=0.5:
        alimentation=alimentation
    elif alimentation<0.5 :
        if hydratation<0.5:
            sante = sante - ((0.5-alimentation)*0.7 + (0.5-hydratation)*0.9)
        else:
            sante = sante - (0.5-alimentation)*0.5
    else:
        sante = sante - (0.6-hydratation)
    if sante <=0:
        sante=0
        c="Mort d'épuisement"
    if sante > 1.0 :
        sante = 1.0
    
    if sante >=0.3 and force<=1.0:
        force=force+0.01
    elif force>=0.1:
        force=force-0.05
    
    
    hydratation=hydratation-0.3
    alimentation=alimentation-0.15
    if hydratation <= 0:
        hydratation =0
        c = "Mort de déshydratation"
        sante = 0
    if alimentation <= 0:
        alimentation = 0
        c = "Mort de faim"
        sante = 0
    return sante,alimentation,hydratation,force,c
# In[251]:
def secouru(p_s, j,p_s_ini,p_s_10):
    """
    float * int -> bool 
    hyp :
    retourne si l agent est secouru par une equipe de secours
    """
    #secouru : bool
    secouru = False
    if j <= 10 :
        p_s = p_s + p_s_ini*0.2
    elif j <= 25 :
        p_s_10 = p_s
    else :
        p_s = p_s - p_s_10*0.2
    
    random5=np.random.random_sample()
    secouru = random5 <= p_s
    return secouru , p_s
# In[252]:
secouru(0.008666657999999999,0,0.00666666,0)
# In[253]:
def model(jour,Lsante):
    """int*list[float]"""
    Ljour=[]
    for i in range(0,jour):
        Ljour.append(i+1)
    plt.bar(Ljour,Lsante , color='green' )
   
# In[254]:
def nourriture_p(p_a, alimentation_p, p_e, hydrat_p):
    """
    float^4 -> float^2
    retourne le niveau d alimentation et d hydratation du predateur
    """
    
    rand = np.random.random_sample()
    if rand <= 1.5*p_a:
        alimentation_p = alimentation_p + 0.15
    if alimentation_p >1 :
        alimentation_p = 1
    if rand <= 1.3*p_e:
        hydrat_p = hydrat_p + 0.4
    if hydrat_p > 1:
        hydrat_p = 1
    return alimentation_p,hydrat_p
# In[255]:
def ev_nourriture_p(alimentation_p, hydrat_p):
    """
    float^2 -> float^2
    retourne le niveau d alimentation du predateur jour apres jour
    """
    alimentation_p = alimentation_p - 0.1
    hydrat_p = hydrat_p - 0.3
    return alimentation_p, hydrat_p
# In[256]:
def mort_p_nourriture(alimentation_p, hydrat_p):
    """
    float^2 -> bool
    retourne si le predateur meurt de faim ou deshydratation
    """
    if alimentation_p <= 0 or hydrat_p <=0 :
        return True
    else :
        return False
# In[257]:
def combat_p_h(force,cap,dang_p):
    """
    float^4 -> float * bool
    retourne l'issue du combat entre le predateur et l'humain
    """
    mort=False
    rand = np.random.random_sample()
    res = (rand*(dang_p+0.55)*(cap-1.65)*(force-1.65))*1.1
        
    
    return res
# In[258]:
def sante_apres_combat(res,alimentation,sante,alimentation_p,sante_p):
    """
    float ^5 -> float ^4 * str
    retourne le niveau de sante et d alimentation en fonction de l'issue du combat, 
    et la cause de la mort si l agent humain meurt
    """
    #c : str
    c="45"
    if res < 0.16 :
        alimentation = alimentation + 0.15
        sante_p = 0
        c = "le prédateur est tué par l'humain"
    elif res < 0.33 :
        alimentation = alimentation + 0.15
        sante = sante - res
        sante_p = 0
        c = " le prédateur est tué par l'humain"
    elif res < 0.5 :
        sante_p = sante_p - (1 - res)
    elif res < 0.66 :
        sante = sante - res
        sante_p = sante_p - (1 - res)
    elif res < 0.8 :
        sante = 0
        sante_p = sante_p - (1 - res)
        c = "l'humain est tué par le prédateur"
    else :
        sante = 0
        c = "l'humain est tué par le prédateur"
    if sante <=0 :
        c ="L'humain succombe de ses blessures"
    return alimentation, sante, alimentation_p, sante_p , c
    
# In[259]:
def sante_fct_hydr_alim_p(alimentation_p, hydrat_p, sante_p):
    """
    float ^3 -> float
    retourne la sante du prédateur en fonction de son alimentation et hydratation
    """
    
    if alimentation_p >= 0.5 and hydrat_p >=0.5:
        if sante_p<0.3:
              sante_p = 0.3
        else:
              sante_p = sante_p + 0.1
    elif alimentation_p < 0.5 :
        if hydrat_p < 0.5:
            sante_p = sante_p - ((0.5-alimentation_p)*0.5 + (0.5-hydrat_p)*0.8)
        else:
            sante_p = sante_p - (0.5-alimentation_p)*0.4
    else:
        sante_p = sante_p - (0.5-hydrat_p)*0.84
    if sante_p > 1.0 :
        sante_p = 1.0
    return sante_p
# In[260]:
#dictionnaire_humain:dict[str:tuple[float,float]]
dictionnaire_humain={}
dictionnaire_humain["professionnel"]=(0.8,0.9)
dictionnaire_humain["bureaucrate"]=(0.2,0.3)
dictionnaire_humain["moyen"]=(0.5,0.5)
dictionnaire_humain["Maxime"]=(0.1,0.1)
#dictionnaire_biome:dict[str:tuple[float,float,int,float,float,float]]
dictionnaire_biome={}
dictionnaire_biome["Amazonie"]=(0.65,5,33,0.7,0.03571428571,0.007142857142)
dictionnaire_biome["Alaska"]=(0.38,3,18,0.6,0.00043185564,0.0086371128)
dictionnaire_biome["France"]=(0.3,0.5,17,0.6,0.03,0.06)
dictionnaire_biome["Sahara"]=(0.25,3,1,0.1,0.00333333,0.00666666)
#dictionnaire_predateur:dict[str:tuple[float]]
dictionnaire_predateur={}
dictionnaire_predateur["jaguar"]=(0.7)      #-> amazonie
dictionnaire_predateur["guepard"]=(0.7)      #-> sahara
dictionnaire_predateur["grizzly"]=(0.9)     #-> alaska
dictionnaire_predateur["sanglier"]=(0.4)    #-> france
# In[261]:
def nouveau_humain(nom,force,cap):
    """
    str * float^2 -> dict[str:tuple[float,float]]
    hyp: len(nom) >= 1 and force >0 and force <1 and cap >0 and cap <1
    retourne le dictionnaire des agents augmenté de l agent créé
    """
    dictionnaire_humain[nom]=(force,cap)
    return dictionnaire_humain
# In[262]:
def nouveau_biome(nom,p_a,p_ap,veg,p_e,p_v,p_s):
    """
    str * float^6 -> dict[str:tuple[float,float,int,float,float,float]]
    hyp: len(nom) >= 1 and 0< p_a <1 and 0< p_ap <1 and 0< veg and 0< p_e <1 and 0< p_v <1 and 0< p_s <1
    retourne le dictionnaire des biomes augmenté du biome créé
    """
    dictionnaire_biome[nom]=(p_a,p_ap,veg,p_e,p_v,p_s)
# In[357]:
nouveau_humain("Jiji1",0.75,0.5)
# In[264]:
def generation_matrice(taille,p_e,nb_pred):
    
    #Création d'une matrice carré, représentant l'environnement, couleurs définies en fonction de la quantité d'eau
    # dans le biome.
    #L_positions:list[list[int,int,int]]
    L_positionsenv=[]
    
    if p_e<0.4:
        couleur=0
    else:
        couleur=-3
    for i in range(0,taille):
        for j in range(0,taille):
            rand = np.random.random_sample()
            if rand<0.34:
                L_positionsenv.append((couleur-2,i,j))
            elif rand<0.67 and rand>0.34:
                L_positionsenv.append((couleur-1,i,j))
            else:
                L_positionsenv.append((couleur,i,j))
    
    #Ajout des prédateurs et de l'humain à la matrice.
    
    nb_pre=nb_pred*taille//10
    #L_inter:list[int,int,int]
    L_inter=[]
    #L_positions:list[list[int,int,int]]
    L_positions=[]
    
    #nb_pre_fi:int
    nb_pre_fi=nb_pre
    
    #i:int
    i=0
    hor=-1
    ver=0
    while i<nb_pre_fi:
        if hor<2:
            hor=hor+1
        else:
            hor=0
            if ver<2:
                ver=ver+1
            else:
                ver=0
        if hor!=1 or ver!=1:
            cori=np.random.randint(hor*(taille/3),(hor+1)*(taille/3))
            corj=np.random.randint(ver*(taille/3),(ver+1)*(taille/3))
            L_positions.append((-10-i,cori,corj))
            i=i+1
    
    L_positions.append((1,taille//2,taille//2))
    
    return L_positions, L_positionsenv
# In[265]:
generation_matrice(30,0.4,5)
# In[390]:
def dessin(L,Lenv,taille,L_posod):
    
    mat=np.zeros((taille,taille))
    for j in range (0,len(Lenv)):
        num,cori,corj=Lenv[j]
        mat[cori,corj]=num
        
    for j in range (0,len(L_posod)):
        num,cori,corj=L_posod[j]
        mat[cori,corj]=num    
    for i in range(0,len(L)):
        num,cori,corj=L[i]
        mat[cori,corj]=num
        
    cmap = colors.ListedColormap(['red','yellowgreen','limegreen', 'olive', 'orange','darkorange',
                                  'goldenrod','blue','black','black'])
    bounds = [-10,-6,-5,-4, -3, -2, -1, 0, 1,2,3]
    norm = colors.BoundaryNorm(bounds, cmap.N)
    print(cmap,bounds,norm)
    fig = plt.figure()
    frame = plt.gca()
    frame.axes.get_xaxis().set_visible(False)
    frame.axes.get_yaxis().set_visible(False)
    grid = plt.imshow(mat, interpolation='nearest', cmap=cmap,
                          norm=norm)
    
    plt.show()
# In[267]:
cmap = colors.ListedColormap(['red','white','yellowgreen','limegreen', 'olive', 'orange','darkorange',
                                 'goldenrod','blue','black','black'])
# In[268]:
mattest,L=generation_matrice(13,0.1,460)
mattest
# In[269]:
dicti={}
dicti[(1,2)]=(5)
dicti[(1,2)]
# In[367]:
def deplacements(chang,L_pos,taille,L_env,jour,L_posod):
    
    ha,ba,ga,da=True,True,True,True
    L_posf=[]
    jour=jour+100
    taille=taille-1
    #nb_pre:int
    nb_pre=0
    Combat=False
    #i:int
    for i in range (0,len(L_pos)):
        num,x,y = L_pos [i]
   
        if num <= -10:
            
            #e:int,fin:int // flag
            e=0
            fin=1
            #xf,yf:int*int //flag
            xf=0
            yf=0
            Li=len(L_pos)
            for j in range (0,len(L_pos)):
                
                numt,xt,yt = L_pos [j]
                if xt==x+1 or xt==x or xt==x-1:
                    if yt == y+1 or yt == y or yt == y-1:
                        if numt == 1:
                            x=xt
                            y=yt
                            fin=0
                        if numt > 1 and fin!=0:
                            if e<numt:
                                e=numt
                                xf=xt
                                yf=yt
                                fin=2
            if j!=0 and fin==0:
                x=xf
                y=yf
            
            if fin==1:
                a=0
                while a==0:
                    n=(np.random.random_sample()*8)//2
                    if n>=3 and y!=0:
                        y=y-1
                        a=1
                    elif n>=2 and x!=taille:
                        x=x+1
                        a=1
                    elif n>=1 and y!=taille:
                        y=y+1
                        a=1
                    elif n>=0 and x!=0:
                        x=x-1
                        a=1
            L_posf.append((num,x,y))
            
        if num==1:
            if chang==True:
                dictitemp={}
                for j in range (0,len(L_env)):
                    numt,xt,yt=L_env[j]
                    dictitemp[(xt,yt)]=(numt)
            
                for j in range (0,len(L_posod)):
                    numt,xt,yt=L_posod[j]
                    dictitemp[(xt,yt)]=(numt)
                
                a=0
                while a==0:
                    n=(np.random.random_sample()*8)//2
                    if n>=2.9 and n<=3.1 and y!=0:
                        if dictitemp[(x,y-1)]<2:
                            L_posod.append((jour,x,y))
                            y=y-1
                            L_posf.append((1,x,y))
                            a=1                                 
                                    
                    elif n>=1.9 and n<=2.1 and x!=taille:
                        if dictitemp[(x+1,y)]<2:
                            L_posod.append((jour,x,y))
                            x=x+1
                            L_posf.append((1,x,y))
                            a=1
                            
                    elif n>=0.9 and n<=1.1 and y!=taille:
                        if dictitemp[(x,y+1)]<2:
                            L_posod.append((jour,x,y))
                            y=y+1
                            L_posf.append((1,x,y))
                            a=1
                    elif n>=-0.1 and n<=0.1 and x!=0:
                        if dictitemp[(x-1,y)]<2:
                            L_posod.append((jour,x,y))
                            x=x-1
                            L_posf.append((1,x,y))
                            a=1
            
                    if x!=0:
                        if dictitemp[(x-1,y)]>=2:
                            ha=False
                    else:
                        ha=False
                    if y!=0:
                        if dictitemp[(x,y-1)]>=2:
                            ga=False
                    else:
                        ga=False
                    if y!=taille:
                        if dictitemp[(x,y+1)]>=2:
                            da=False
                    else:
                        da=False
                    if x!=taille:
                        if dictitemp[(x+1,y)]>=2:
                            ba=False
                    else:
                        ba=False
                    if ha==False and ba==False and ga==False and da==False:
                        n=np.random.random_sample()
                        if n>0.5:
                            if y!=0:
                                L_posod.append((jour,x,y))
                                y=y-1
                                L_posf.append((1,x,y))
                                a=1
                            else:
                                L_posod.append((jour,x,y))
                                y=y+1
                                L_posf.append((1,x,y))
                                a=1
                        else:
                            if x!=0:
                                L_posod.append((jour,x,y))
                                x=x-1
                                L_posf.append((1,x,y))
                                a=1
                            if x!=taille:
                                L_posod.append((jour,x,y))
                                x=x+1
                                L_posf.append((1,x,y))
                                a=1
            if chang==False:
                L_posf.append((1,x,y))
            for k in range (0,len(L_pos)):
                numf,xf,yf=L_pos[k]
                if xf==x and yf==y and numf<=-10:
                    Combat=True
                        
    
    return L_posf,Combat,L_posod
# In[416]:
def mort(L):
    xf=0
    yf=0
    for i in range(0,len(L)):
        num,x,y=L[i]
        if num==1:
            xf=x
            yf=y
    for j in range(0,len(L)):
        num,x,y=L[j]
        if x==xf and yf==y:
            del L[i]
    return L
# In[360]:
def simul_depla(L_env,L,change,taille,j,L_posod):
    
    L , Combat , L_posod = deplacements(change,L,taille,L_env,j,L_posod) 
    #dessin(L,L_env,taille, L_posod)
    
    return L,Combat,L_posod
# In[406]:
def simulation_survie(agent,biome,predateur,taille):
    """str*str*dict[str:tuple[float,float]]*dict[str:tuple[float,float,int,float,float,float]] -> int """
    
    
    #c : cause de la fin
    c = ""
    #j : compteur jour
    j = 0
    #jour_r:float
    jour_r=-10
    #abri:bool
    abri=False
    #sauve:bool
    sauve=False
    #sourceinf:bool
    source_inf=False
    #sante:float
    sante=1.0
    #hydrat:float
    hydrat=1.0
    #alimentation:float
    alimentation=1.0
    #alimentation_p:float
    alimentation_p=1.0
    #hydrat_p:float
    hydrat_p=1.0
    #sante_p:float
    sante_p=1.0
    
    #Lsante:list[float]
    Lsante=[]
    Leau=[]
    
    dang_p = dictionnaire_predateur[predateur]
    force , capadap = dictionnaire_humain[agent]
    p_a , nb_p, veg , p_e , p_v , p_s = dictionnaire_biome[biome]
    vegr=veg
    p_s_ini = p_s
    p_s_10=p_s
    
    
    L_posod=[]
    L_pos,L_env = generation_matrice (taille, p_e, nb_p)
    
    while sante > 0 and sauve != True:
  
        chang=False
        jour_r , abri , sauve , source_inf = construction_abri(capadap , source_inf , vegr , veg , p_v , jour_r , abri)
        
        if sauve==True:
            c='sauve'
            return j, c,sante
        if vegr==0 :
            chang=True
        
        sourceinf , hydrat  = trouver_eau(p_e , capadap , source_inf , hydrat)
        
        #alimentation , sante , c  = inter_anim(p_a, force, capadap, alimentation, sante, c)
        
        
        
        
        if c != "":
            print(model(j,Lsante),Lsante)
            return j, c,sante
        
        alimentation , vegr = inter_veget(veg,alimentation,capadap,vegr)
        
        sante , alimentation , hydrat , force , c = sante_fct_hydr_alim(alimentation, hydrat, sante,abri,force,c)
        
        sauve , p_s = secouru (p_s,j,p_s_ini,p_s_10)
        
        #alimentation_p,hydrat_p = nourriture_p(p_a, alimentation_p, p_e, hydrat_p)
        
        alimentation_p, hydrat_p = ev_nourriture_p(alimentation_p, hydrat_p)
        
        sante_fct_hydr_alim_p(alimentation_p, hydrat_p, sante_p)
        
 
        L_pos , Combat ,L_posod = simul_depla(L_env,L_pos,chang,taille,j,L_posod)
        
        if Combat == True:
            
            res = combat_p_h(force,capadap,dang_p,)
            sante_p = alimentation, sante, alimentation_p, sante_p , b = sante_apres_combat(res,alimentation,sante,alimentation_p,sante_p)
            if b=="le prédateur est tué par l'humain":
                L_pos=mort(L_pos)
            if b!="45":
                c=b
                return j,c,sante,"fd"
        Lsante.append(sante)
        Leau.append(hydrat)
        #Définition de la capacité de survie a x jour
        
        if j==10:
            p_s_10 = p_s
        
        #Augmentation de la capacité d'adaptation
        if capadap<1.0:
            capadap=capadap+0.01
       
        
        j=j+1
        alimentation=alimentation-0.01
        hydrat=hydrat-0.01
        
        
    #print(model(j,Lsante),Lsante)
    if sauve==True:
        c="Sauvé!"
    return j, c,sante
# In[327]:
def test(a,b,c):
    comp=0
    while a!=0:
        aa,ab,ah=simulation_survie(b,c)
        if ah!=0:
            comp=comp+1
        a=a-1
    return simulation_survie(b,c),comp
# In[369]:
simulation_survie("moyen","Sahara","jaguar",20)
# In[430]:
a=20
while a!=0:
    print(simulation_survie("moyen","Amazonie","guepard",10))
    a=a-1
    