# artrabeamer
## A Beamer template for easily positioning and manipulating content

<h1 align="center">
<img width="100%" src="https://github.com/mohuangrui/mohuangrui/blob/main/gallery/artrabeamer_english.gif" alt="Beamer English">
<img width="100%" src="https://github.com/mohuangrui/mohuangrui/blob/main/gallery/artrabeamer_chinese.gif" alt="Beamer Chinese">
</h1>

## Compilation: requires LaTeX environment
* Just compile like an ordinary Beamer/LaTeX: `pdflatex+biber+pdflatex+pdflatex`
* Switch to Chinese: just add the "CJK" option in "artrabeamer.tex"
```Tex
\usepackage[CJK,biber,authoryear,tikz,table,xlink]{Style/artrabeamer}}
```
* Many other functionalities: check the available options in "artrabeamer.tex" below the line
```Tex
\usepackage[biber,authoryear,tikz,table,xlink]{Style/artrabeamer}
```

## Useful commands added to generic LaTeX
```Tex
\enorcn{English}{Chinese}: automatically switch between English and Chinese versions
\tikzart[t=m]{}}: draw coordinate system to help you position contents
\tikzart[t=p,x=-7,y=3,w=4]"comments"{figname}}: position a picture named "figname" at location "(x,y)" with width "w=4" and comments below the picture.
\tikzart[t=o,x=0,y=-0.8,s=0.8]{objects-such-as-tikz-diagrams}}: position objects at location "(x,y)" with scaling "s=0.8"
\tikzart[t=v,x=9.5,y=-6.5,w=0.5]{Video/vortex_preserve_geo.mp4}[\includegraphics{cover_image}]}: position a video at location "(x,y)" with a cover image of width "w=0.5"
\lolt{lowlight}}, \hilt{highlight}: make the item show in different color when in different state
```