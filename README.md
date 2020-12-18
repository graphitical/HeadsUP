# HeadsUP: Improving Document Structure Recognition to Support Automatic Accessible PDF Generation
by [Venkatesh Potluri](https://venkateshpotluri.me), [Daniel Revier](https://make4all.org/portfolio/daniel-revier/) and [Taylor Gotfrid](https://make4all.org/portfolio/taylor-gotfrid/)

[![Watch the video](https://img.youtube.com/vi/GpforMeYBxE/hqdefault.jpg)](https://www.youtu.be/GpforMeYBxE)

## Abstract
PDFs are often produced with absent or incorrect accessibility tags resulting in missing information about document structure, tables, reading order, images, etc. These missing tags can result in an incomprehensible reading experience for screen reader users. Identifying heading levels will improve the overall readability of the document as well as the logical formatting of the document. For this project, we developed a dataset for a document analysis RCNN (region based convolutional neural network) to improve heading and heading level identification. We first created our dataset composed of PDFs and the corresponding HTML version of the PDFs from the CHI 2019 conference proceedings. We use a detectron2 implementation of an RCNN model pre-trained on the PubLayNet dataset to extract labels (e.g. title, text, figure), then correlate those extracted features via optical character recognition (OCR) with heading levels using the corresponding HTML files. For future work we hope to use transfer learning to retrain PubLayNet to include heading level detection.

## Problem Statement
If given research papers in PDF and HTML format, can we use transfer learning to improve upon heading and heading level detection by using transfer learning on the Detectron2 PubLayNet RCNN model.

## Dataset
Our dataset is based on the CHI 2019 conference proceedings. Over the last few years, the ACM has been taking steps towards providing publications in alternative, accessible formats (e.g. HTML, e-reader) through the introduction of their [TAPS (The ACM Publication System)](https://www.acm.org/publications/taps/taps-best-practices) publication workflow, and an [all-encompassing publication template](https://www.acm.org/publications/proceedings-template) for all conferences. Consequently, conferences that adopted this workflow have PDF (which may or may not be tagged), and accessible HTML versions (which have defined header levels by default) of their proceedings.

For our dataset we have 465 PDF/HTML document pairs for a total 5,841 pages painstakingly collected from the Association of Computing Machinery (ACM) Digital Library.

Through this effort, we contribute:
* A pipeline to augment a state-of-the art document layout analysis dataset, PubLayNet, with additional data to detect heading level information.
* Additional data to the PubLayNet dataset created using our pipeline.

## Related Work
The [Detectron2](https://github.com/facebookresearch/detectron2) RCNN we used in our project is from prior work. We used the [Detectron2 RCNN pre-trained](https://github.com/hpanwar08/detectron2) on part of the [PubLayNet dataset](https://github.com/ibm-aur-nlp/PubLayNet). 

There has been a lot of research examining how to construct logical reading order or to detect headers in pdf documents using machine learning and neural networks. Previous research has explored how ML can be used to detect headings and section boundaries [1]. Neural networks have also been used to section, tag, and create logical reading structure for pdf documents. Recent work has explored how to use RCNNs to tag pdf document text as title, text, figure, label, or table. However, this method does not take into account heading level and assumes all headers are titles [3]. Another study used html markup to extract the logical structure of a document through using heading markup tags [3]. We hoped to combine these methods to help determine heading level to improve the overall accuracy of the RCNN we chose to use.

## Methodology
Once we determined our project’s pipeline, we began building our dataset with the CHI 2019 conference proceedings papers.
### Data collection
To build our dataset we downloaded both the PDF and HTML version of all papers presented at this conference; however, we did encounter some difficulties when creating our dataset. First we encountered difficulties when trying to download the PDFs and HTML versions from the ACM Digital Library. The ACM Digital Library (ACM DL) provided full proceeding  links. These however did not include the HTML versions of the papers. Consequently, we contacted ACM to get access to the HTML proceedings, attempted to manually download and automatically scrape ACM DL for the HTML papers.  However, ACM would block our IP addresses for several hours after a certain number of downloads were made over a certain period of time. We never figured out this magic “number of downloads over a certain period of time” ratio that would not cause this to occur. Due to this problem as well as the time constraints of the project we only used one year of one conference’s proceedings to build our dataset with. In the future we hope to expand our dataset to include CHI 2020 as well as the proceedings from ASSETS 2019-2020 which also have PDF/HTML paper pairs.

### Creating the dataset
First, we ran our CHI data through the Detectron2 version of PubLayNet network to give us annotations for elements (e.g. title, figure, text, list, table) within the PDF. Then we crop the annotations that were labeled as a “title” from the previous step to determine the text labeled as a title. Afterwards we cross correlate this extracted text from the png with the HTML version of the paper to establish a specific heading level for each specified title.
## Future Work
While our exploration for the scope of this class project has been preliminary, we have a pipeline in place to experiment with more ACM HTML paper data (which have the right heading tags) as they become available and we get access to them. Our eventual goals are both exploratory (research) and translatory (deploying our work to benefit end-users). Our exploratory goals involve experimentation of different approaches to produce a state-of-the art heading detection model, and our translatory goals involve integrating these state-of-the art models into existing solutions that automate document accessibility.
## References
[1] Manabe, T., & Tajima, K. (2015). Extracting logical hierarchical structure of HTML documents based on headings. Proceedings of the VLDB Endowment, 8(12), 1606-1617.  
[2] Tuarob, S., Mitra, P., & Giles, C. L. (2015, August). A hybrid approach to discover semantic hierarchical sections in scholarly documents. In 2015 13th international conference on document analysis and recognition (ICDAR) (pp. 1081-1085). IEEE.  
[3] Zhong, X., Tang, J., & Yepes, A. J. (2019, September). Publaynet: largest dataset ever for document layout analysis. In 2019 International Conference on Document Analysis and Recognition (ICDAR) (pp. 1015-1022). IEEE.  
