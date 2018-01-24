def xep_chong_du_lieu(data_goc, data_moi, vi_tri):
  i = vi_tri
  for x in data_moi:
    if i < len(data_goc):
      data_goc[i] = x
    else:
      data_goc.append(x)
    i+=1

a=[1,2,3,4,5,6]
b=[11,22,33,44]
xep_chong_du_lieu(a,b,0)
print(a)
xep_chong_du_lieu(a,b,2)
print(a)
