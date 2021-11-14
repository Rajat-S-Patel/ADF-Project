from django import template

register = template.Library()

@register.filter
def percentage(value):
    return format(value, ".2%")

@register.filter
def readable(value):
    if(value < 10000) :return ""+ str(value)
    elif(value < 10**5):return ""+ str(round(value/1000),2) + " K"
    elif(value< 10**7):return ""+str(round(value/100000,2)) + " L"
    elif(value < 10**13):return ""+str(round(value/(10**7),2))+" Cr"
    else : return ""+str(round(value/(10**14),2)) +' LCr'

@register.filter
def acronym(value):
    if(len(value)<16): return value
    else:
        res=""
        for i in value.split():
            res+=i.upper()[0]
        return res

     