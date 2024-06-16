Reranker Experimentation SummaryDataset DescriptionOur dataset consists of a set of queries and their corresponding paragraphs. Each paragraph is labeled as either "related" or "not related" to the query. The dataset is organized as follows:Total Queries: 3Total Paragraphs:Query 1: 5 paragraphsQuery 2: 19 paragraphsQuery 3: 20 paragraphsEach paragraph contains an ID, the paragraph text, and a "related" flag indicating its relevance to the query.Example Query and Paragraphs:{
  "query": "What are the benefits of health insurance?",
  "paragraphs": [
    {
      "id": 1,
      "text": "Health insurance provides financial coverage for medical expenses such as doctor visits, hospital stays, and medications.",
      "related": true
    },
    {
      "id": 2,
      "text": "Life insurance policies pay a lump sum to beneficiaries upon the policyholder's death.",
      "related": false
    },
    {
      "id": 3,
      "text": "With health insurance, you can access preventive services like vaccinations and screenings at no additional cost.",
      "related": true
    },
    {
      "id": 4,
      "text": "Car insurance covers damages to your vehicle in case of an accident.",
      "related": false
    },
    {
      "id": 5,
      "text": "Health insurance plans often cover a range of treatments, including surgeries and emergency care.",
      "related": true
    }
  ]
}Experimentation DetailsWe tested several rerankers to evaluate their accuracy and response time. The rerankers tested were:ColBERTBGEFlashRankZsMiniLLMFlashRankFlanT5Each query and its related paragraphs were sent at once to the different models for reranking.The experimentation was carried out on a Databricks notebook with the following configuration:Databricks Runtime Version: [Insert Version]Cluster Configuration:Driver Type: [Insert Driver Type]Worker Type: [Insert Worker Type]Number of Workers: [Insert Number of Workers]The code for the experimentation is available on Bitbucket. You can find the code here.Results SummaryThe performance of each reranker was measured in terms of response time and reranker score. Below is a summary of the findings:FlashRankZsMiniLLM and BGE were found to be the most accurate rerankers.FlashRankZsMiniLLM was the fastest reranker.Detailed Results:ColBERTResponse Time: [Insert Response Time]Reranker Score: [Insert Score]BGEResponse Time: [Insert Response Time]Reranker Score: [Insert Score]FlashRankZsMiniLLMResponse Time: [Insert Response Time]Reranker Score: [Insert Score]FlashRankFlanT5Response Time: [Insert Response Time]Reranker Score: [Insert Score]ConclusionBased on the results of our experimentation, FlashRankZsMiniLLM is recommended for scenarios where both accuracy and speed are crucial. BGE also performs well in terms of accuracy and can be considered as an alternative.
