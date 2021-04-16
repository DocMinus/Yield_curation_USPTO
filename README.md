[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
# Yield Curation of USPTO rsmi/csv files <br>(Lowe/Schwaller datasets)

## About
As the title states, these scripts curate (deconvolute) the yield columns contained in aforementioned public data sets.<br>
First is the so-called "Lowe dataset": https://figshare.com/articles/dataset/Chemical_reactions_from_US_patents_1976-Sep2016_/5104873
Second, the so called "Schwaller dataset" which is a continuation of above set: https://pubs.rsc.org/en/content/articlelanding/2018/SC/C8SC02339E
<br>(This in turn uses the curated set disclosed by Jin and coworkers, see https://dl.acm.org/doi/10.5555/3294996.3295021)

All credit for these curation goes to the authors in above links, as well as the appropriate licensing info for the data.<br>
<br>
These two data-sets have two pre-curated columns of text mined yield versus calculated yield. Many entries don't contain 
any, partial, or incorrect numbers. For the majority of reaction analysis when having only the yield as available outcome,
that information becomes useless since there is no correlation to reaction conditions. Thus, by correcting & eliminating such 
entries, noise in the data set is reduced. <br> The new datasets contain approx. only 50% of the original dataset!

### Python scripts
Two scripts are available:<br>
- *curate_yield_cropped.py*: this removes incomplete/missing/wrong entries entirely, 
  incl. the patent/paragraf/yield columns and corresponds to the data available on Figshare.
For users who don't agree to the filtration and want to keep all data:  
- *curate_yield_full.py*: curates the yield, but keeps all other data (incl. columns) intact.  

### Requirements
Python 3.6 or higher. Only standard numpy/pandas libraries are used.<br>

### Usage
Change the path & file names in the script to your locations. 
The scripts are light weight without any error checking or cmd line inputs, etc.

### Notes on the datasets
#### Columns in Schwaller dataset: (Lowe dataset marked with *)
-    Source                   
-    Target                   
-    CanonicalizedReaction    
-    OriginalReaction (= ReactionSmiles*)         
-    PatentNumber*            
-    ParagraphNum*             
-    Year*                     
-    TextMinedYield*           
-    CalculatedYield*          

#### Majority of text tokens that appear in yield columns
*TextMinedYield*
- x%
- \> or \< x% & >= x%
- ~x%
- ~x to y&
- x.xx%
- negative numbers

*CalculatedYield*
- x.x%
- also with some negative values or values >> 100%

#### Output 
new columns (independent of filtration of input columns)
- ID (optional)
- Yield (the curated one, in %)

#### How the yield is curated
- Although some values look as if they are due to calculation error (factor 10 or 100), or a typo (missing .),
  this remains an assumption and thus such numbers have to been seen as faulty and dismissed.
- If neither yield type exists or if the value > 100% or negative, then it is set to 0.
- If a value is only in one column, that value is used
- If value is available in both, then the larger value is used
- Range x to y%: the largest value y% is used
- Since 0 corresponds to basically none existent or faulty data, these are dismissed (filtered out) entirely.
- An estimated <0.1% of incorrect entries are not corrected and end up being also filtered out.

#### Reference
figshare: https://doi.org/10.6084/m9.figshare.14414039

#### License
MIT license, see license file for details.
