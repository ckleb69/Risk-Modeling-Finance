Workflow of the files go 

“Extract and Process Data” creates Clean WRDS and Descriptive L moments (Extracted data for 24 equities from daily 2000-2024, basic data cleaning for the EGARCH Models)

“NewEGARCHnormal/student13” creates respective CSV  (Creates EGARCH (1,3) Normal and Student T. scaled to 10^6 to prevent convergence and computed persistence)

“New_CompareNandT(13)” creates respective CSV (Compared EGARCH and student via AIC and BIC, student won 23/24)

“Process_Studentt” creates NewEGARCHstudent and Student residuals folder (Computed the residuals for each stock for each entry)

“compare residual” creates Residualonly... CSV   (Compared residuals of Pearson VII and Student-t, had to use MLE instead of L moments for the pearson calculation because of coding limitations)

“visuals” to “Residual fit plot”   (Nice Visuals of distribution)

“boots” to bootstrap robustness 

“bootsVar” to Var Exceed 

“Var plot” to Var exceed plot 

“Treasure” to Fred...   (3 month treasury bills from fed reserve)

"boots Interest" to Rate Regmine    (bootstrap simulation with the interest rates)

Row 3- Extracted data for 24 equities from daily 2000-2024, basic data cleaning for the EGARCH Models 
Row 4- Creates EGARCH (1,3) Normal and Student T. scaled to 10^6 to prevent convergence and computed persistence
Row 5- Compared EGARCH and student via AIC and BIC, student won 23/24
Row 6- Computed the residuals for each stock for each entry
Row 7 - Compared residuals of Pearson VII and Student-t, had to use MLE instead of L moments for the pearson calculation because of coding limitations
Row 8 - Nice Visuals of distribution
Row 9-11 - Ignore for now
Row 11* - 3 month treasury bills from fed reserve
Row 12* - bootstrap simulation with the interest rates
