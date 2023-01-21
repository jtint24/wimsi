# wimsi
Wikipedia-Integrated Map Structuring Interface

A tool to build Jotted maps for practically any topic. This includes grouped, connected nodes, organized sources, and intelligent summaries

## Layers

- Graph creation
  - Wikipedia articles are used to build one universal graph of knowledge, showing relations between topics based on co-occurrence and semantic similarity
- Map extraction
  - From the universal graph, the skeleton of a Jotted map can be extracted which center on nearly any node. This is done by apply a breadth-first search to the graph and getting the discovery tree. 
- Sourcing
  - Sources from a given vertex (sources from the original article on the topic) must be trimmed and organized. This is done by categorizing similar sources and using heuristics to find the best sources in each category
- Summarization
  - Summaries can be created from sources or from original articles

## To-do

- [ ] Graph Creation
  - [x] Pull related Wikipedia articles
  - [x] Mirror articles that redirect to each other
  - [x] Construct graph using BFS of topics
- [ ] Map Extraction
  - [x] Find discovery tree of graph
  - [ ] Enhance discovery time calculation with semantic similarity to root node
- [ ] Sourcing
  - [x] Pull Sources from Topics
  - [ ] Write code to compare two sources for semantic similarity
  - [x] Develop algorithm for efficient grouping that minimizes number of groups while also minimizing maximum semantic difference within a group
  - [ ] Develop heuristics list for evaluating source quality
  - [ ] Finish Source Filtering Algorithm
- [ ] Summarization
  - [x] Get Wikipedia Summary
  - [ ] More sophisticated/brilliant method:
    - [ ] Get key sentences from sources
    - [ ] Synthesize/fuse key sentences



## AI Problem Areas

<ol type="a">
  <li>Figuring out how similar two vertices are to one another without using hyperlink frequency, which is heavily flawed (do this by getting keywords and running cosine similarity ?). We use this in figuring out when branches of a tree should terminate</li>
  <li>Calculating how relevant a hyperlink is to an article. We can apply a keyword search and run the priority queue by the entropy of the keyword, but that has downsides for short articles. We can pull the text of the linked article and reduce this to a class A problem.</li>
  <li>Finding a way to get good resources for each vertex, not just topic names. Right now, each vertex is associated to a Wikipedia article, so sources are built in from the get-go, but these sources aren't filtered, sorted, or validated in any way. The result is 100’s of sources per vertex sometimes without a solid basis. How do we go from this to a curated list of just a few high-quality sources? There are 3 subproblems:</li>
  <ol type = "1">
  <li>Filtering out sources that seem to be irrelevant, fraudulent, incorrect, or out-of-date. This can be done heuristically through checking if the source is from a trusted domain, (use a whitelist?), date on the source, and keyword similarity between source and main article, similar to problem A. How do we measure sources that are books or inaccessible (behind paywall)? We could just discard them; they wouldn’t be open to users anyways.</li>
  <li>Sorting sources into categories based on what they are specifically used to show or prove. This could be done later.</li>
  <li>Once sorting is done, removing the worst redundant sources. This could be probably through a similar process as C-1, by calculating a “quality score” for each source and removing all but the best source or two in each category. Also could involve some kind of relationship score that we calculate in C-2. Could also just look at link frequency. </li>
  </ol>
  </li>
  <li>Getting summary information for a vertex. Right now we just use wikipedia's built in summary feature, which is okay, but can be verbose and not geared towards general knowledge. It would be cool to have summaries adapt to skill level, so what we could even do is pull pages from the web that summarize the sources and get a summary from one that has a readability index closest to the user's reading level. That would be compute heavy but would be super cool. We could cache various articles to offload the work onto initial calculations (pros are faster access times for users but slow time to build the trees and also much more space required to store them and the info won't update unless we do it manually) or we could do it ad hoc. Better solution than either of those two probably needed, we could stick with wikipedia summaries for now. Might be a way to use a similar system as C-2/C-3 to pull text directly from good relevant sources and eliminate redundancy.</li>
</ol>
