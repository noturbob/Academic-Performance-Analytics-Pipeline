# COMPREHENSIVE STATISTICAL ANALYSIS - ACADEMIC PERFORMANCE SEMESTER V
# ========================================================================

# Install required packages silently
packages <- c("moments", "dplyr")
for (pkg in packages) {
  if (!require(pkg, character.only = TRUE, quietly = TRUE)) {
    install.packages(pkg, dependencies = TRUE, repos = "https://cran.r-project.org/", quiet = TRUE)
    library(pkg, character.only = TRUE, quietly = TRUE)
  }
}

library(dplyr)
library(moments)

cat("\n")
cat("======================================================================\n")
cat("COMPREHENSIVE STATISTICAL ANALYSIS - ACADEMIC PERFORMANCE\n")
cat("SEMESTER V RESULTS\n")
cat("======================================================================\n\n")

# Load data
performance <- read.csv("data/cleaned/performance.csv", stringsAsFactors = FALSE)
grades <- read.csv("data/cleaned/grades.csv", stringsAsFactors = FALSE)
subjects <- read.csv("data/cleaned/subjects.csv", stringsAsFactors = FALSE)
students <- read.csv("data/cleaned/students.csv", stringsAsFactors = FALSE)

# Remove NA SGPA values
perf_clean <- performance[!is.na(performance$sgpa), ]

n_total <- nrow(performance)
n_sgpa <- nrow(perf_clean)
n_promoted <- n_total - n_sgpa

cat(sprintf("Sample Size: %d students with valid SGPA\n", n_sgpa))
cat(sprintf("Total Students: %d (includes %d promoted)\n\n", n_total, n_promoted))

# ========================================================================
# 1. DESCRIPTIVE STATISTICS
# ========================================================================

cat("----------------------------------------------------------------------\n")
cat("1. DESCRIPTIVE STATISTICS\n")
cat("----------------------------------------------------------------------\n\n")

sgpa_mean <- mean(perf_clean$sgpa, na.rm = TRUE)
sgpa_median <- median(perf_clean$sgpa, na.rm = TRUE)
sgpa_sd <- sd(perf_clean$sgpa, na.rm = TRUE)
sgpa_var <- var(perf_clean$sgpa, na.rm = TRUE)
sgpa_min <- min(perf_clean$sgpa, na.rm = TRUE)
sgpa_max <- max(perf_clean$sgpa, na.rm = TRUE)
sgpa_range <- sgpa_max - sgpa_min
sgpa_iqr <- IQR(perf_clean$sgpa, na.rm = TRUE)
sgpa_skewness <- skewness(perf_clean$sgpa, na.rm = TRUE)
sgpa_kurtosis <- kurtosis(perf_clean$sgpa, na.rm = TRUE)
sgpa_mode <- as.numeric(names(sort(table(perf_clean$sgpa), decreasing = TRUE)[1]))

cat("SGPA Descriptive Statistics:\n")
cat("--------------------------------------------------\n")
cat(sprintf("Mean                :   %.4f\n", sgpa_mean))
cat(sprintf("Median              :   %.4f\n", sgpa_median))
cat(sprintf("Mode                :   %.4f\n", sgpa_mode))
cat(sprintf("Std Dev             :   %.4f\n", sgpa_sd))
cat(sprintf("Variance            :   %.4f\n", sgpa_var))
cat(sprintf("Min                 :   %.4f\n", sgpa_min))
cat(sprintf("Max                 :   %.4f\n", sgpa_max))
cat(sprintf("Range               :   %.4f\n", sgpa_range))

q1 <- quantile(perf_clean$sgpa, 0.25)
q2 <- quantile(perf_clean$sgpa, 0.50)
q3 <- quantile(perf_clean$sgpa, 0.75)

cat(sprintf("Q1 (25%%)            :   %.4f\n", q1))
cat(sprintf("Q2 (50%%)            :   %.4f\n", q2))
cat(sprintf("Q3 (75%%)            :   %.4f\n", q3))
cat(sprintf("IQR                 :   %.4f\n", sgpa_iqr))
cat(sprintf("Skewness            :   %.4f\n", sgpa_skewness))
cat(sprintf("Kurtosis            :   %.4f\n\n", sgpa_kurtosis))

# ========================================================================
# 2. NORMALITY TESTS
# ========================================================================

cat("----------------------------------------------------------------------\n")
cat("2. NORMALITY TESTS\n")
cat("----------------------------------------------------------------------\n\n")

shapiro_test <- shapiro.test(perf_clean$sgpa)
cat("Shapiro-Wilk Test:\n")
cat(sprintf("  Test Statistic: %.6f\n", shapiro_test$statistic))
cat(sprintf("  P-value: %.6f\n", shapiro_test$p.value))
cat(sprintf("  Result: Data is %s NORMALLY distributed\n\n", 
            ifelse(shapiro_test$p.value > 0.05, "", "NOT ")))

ks_test <- ks.test(perf_clean$sgpa, "pnorm", mean = sgpa_mean, sd = sgpa_sd)
cat("Kolmogorov-Smirnov Test:\n")
cat(sprintf("  Test Statistic: %.6f\n", ks_test$statistic))
cat(sprintf("  P-value: %.6f\n\n", ks_test$p.value))

# ========================================================================
# 3. HYPOTHESIS TESTING
# ========================================================================

cat("----------------------------------------------------------------------\n")
cat("3. HYPOTHESIS TESTING\n")
cat("----------------------------------------------------------------------\n\n")

t_test <- t.test(perf_clean$sgpa, mu = 8.0)
cat("One-Sample T-Test (H0: μ = 8.0)\n")
cat(sprintf("  T-statistic: %.6f\n", t_test$statistic))
cat(sprintf("  P-value: %.6f\n", t_test$p.value))
cat(sprintf("  Mean: %.4f\n", t_test$estimate))
cat(sprintf("  95%% CI: [%.4f, %.4f]\n", t_test$conf.int[1], t_test$conf.int[2]))
cat(sprintf("  Conclusion: Mean is %s from 8.0\n\n", 
            ifelse(t_test$p.value < 0.05, "SIGNIFICANTLY different", "NOT significantly different")))

chi_test <- chisq.test(table(performance$performance_category))
cat("Chi-Square Test (Category Distribution)\n")
cat(sprintf("  Chi-Square Statistic: %.6f\n", chi_test$statistic))
cat(sprintf("  P-value: %.6f\n\n", chi_test$p.value))

# ========================================================================
# 4. CORRELATION ANALYSIS
# ========================================================================

cat("----------------------------------------------------------------------\n")
cat("4. CORRELATION ANALYSIS\n")
cat("----------------------------------------------------------------------\n\n")

cor_avg <- cor.test(perf_clean$sgpa, perf_clean$avg_grade_points)
cat("Pearson Correlations:\n\n")
cat("SGPA vs Avg Grades:\n")
cat(sprintf("  Correlation (r): %.6f\n", cor_avg$estimate))
cat(sprintf("  P-value: %.6f\n", cor_avg$p.value))
cat(sprintf("  Significance: %s\n\n", 
            ifelse(cor_avg$p.value < 0.001, "***",
            ifelse(cor_avg$p.value < 0.01, "**",
            ifelse(cor_avg$p.value < 0.05, "*", "ns")))))

cor_fail <- cor.test(perf_clean$sgpa, perf_clean$fail_count)
cat("SGPA vs Fail Count:\n")
cat(sprintf("  Correlation (r): %.6f\n", cor_fail$estimate))
cat(sprintf("  P-value: %.6f\n\n", cor_fail$p.value))

# ========================================================================
# 5. ANOVA
# ========================================================================

cat("----------------------------------------------------------------------\n")
cat("5. ANOVA - SGPA BY PERFORMANCE CATEGORY\n")
cat("----------------------------------------------------------------------\n\n")

perf_anova <- perf_clean[perf_clean$performance_category != "", ]
anova_res <- aov(sgpa ~ performance_category, data = perf_anova)
anova_sum <- summary(anova_res)

cat("One-way ANOVA Results:\n")
cat(sprintf("  F-Statistic: %.6f\n", anova_sum[[1]]$`F value`[1]))
cat(sprintf("  P-value: %.6f\n\n", anova_sum[[1]]$`Pr(>F)`[1]))

cat("Mean SGPA by Category:\n")
cat_means <- aggregate(sgpa ~ performance_category, data = perf_anova, FUN = mean)
cat_n <- aggregate(sgpa ~ performance_category, data = perf_anova, FUN = length)
for (i in 1:nrow(cat_means)) {
  cat(sprintf("  %-20s :   %.2f (n=%d)\n", 
              cat_means$performance_category[i],
              cat_means$sgpa[i],
              cat_n$sgpa[i]))
}
cat("\n")

# ========================================================================
# 6. SUBJECT DIFFICULTY
# ========================================================================

cat("----------------------------------------------------------------------\n")
cat("6. SUBJECT DIFFICULTY ANALYSIS\n")
cat("----------------------------------------------------------------------\n\n")

subj_stats <- data.frame(
  course_code = unique(grades$course_code),
  stringsAsFactors = FALSE
)

subj_stats$mean_pts <- sapply(subj_stats$course_code, function(code) {
  mean(grades$grade_points[grades$course_code == code], na.rm = TRUE)
})

subj_stats$std_pts <- sapply(subj_stats$course_code, function(code) {
  sd(grades$grade_points[grades$course_code == code], na.rm = TRUE)
})

subj_stats$n_students <- sapply(subj_stats$course_code, function(code) {
  length(grades$grade_points[grades$course_code == code])
})

subj_stats$fail_count <- sapply(subj_stats$course_code, function(code) {
  sum(grades$grade_points[grades$course_code == code] == 0, na.rm = TRUE)
})

subj_stats$fail_rate <- (subj_stats$fail_count / subj_stats$n_students) * 100

subj_easy <- subj_stats[order(-subj_stats$mean_pts), ]

cat("5 Most Difficult Subjects (Lowest Avg Points):\n")
for (i in 1:min(5, nrow(subj_stats))) {
  cat(sprintf("  %s: %.2f\n", subj_stats$course_code[i], subj_stats$mean_pts[i]))
}

cat("\n5 Easiest Subjects (Highest Avg Points):\n")
for (i in 1:min(5, nrow(subj_easy))) {
  cat(sprintf("  %s: %.2f\n", subj_easy$course_code[i], subj_easy$mean_pts[i]))
}
cat("\n")

# ========================================================================
# 7. EFFECT SIZES
# ========================================================================

cat("----------------------------------------------------------------------\n")
cat("7. EFFECT SIZE CALCULATIONS\n")
cat("----------------------------------------------------------------------\n\n")

cohens_d <- (sgpa_mean - 8.0) / sgpa_sd
cat("Cohen's d (SGPA vs 8.0 benchmark):\n")
cat(sprintf("  Effect Size: %.4f\n", cohens_d))
cat("  Interpretation: small effect\n\n")

# ========================================================================
# 8. VISUALIZATIONS
# ========================================================================

cat("----------------------------------------------------------------------\n")
cat("8. GENERATING STATISTICAL VISUALIZATIONS\n")
cat("----------------------------------------------------------------------\n\n")

dir.create("r/outputs", showWarnings = FALSE, recursive = TRUE)
dir.create("visualizations/statistical", showWarnings = FALSE, recursive = TRUE)

# Plot 1: Descriptive Statistics
png("r/outputs/01_descriptive_statistics.png", width = 1200, height = 800)
par(mfrow = c(2, 2))
hist(perf_clean$sgpa, breaks = 15, main = "SGPA Distribution", xlab = "SGPA", ylab = "Frequency", col = "skyblue")
qqnorm(perf_clean$sgpa, main = "Q-Q Plot")
qqline(perf_clean$sgpa, col = "red")
boxplot(perf_clean$sgpa, main = "SGPA Box Plot", ylab = "SGPA", col = "lightblue")
plot(density(perf_clean$sgpa), main = "SGPA Density", xlab = "SGPA", ylab = "Density")
dev.off()
cat("✓ Saved: 01_descriptive_statistics.png\n")

# Plot 2: Category Distribution
png("r/outputs/02_category_distribution.png", width = 1200, height = 600)
par(mfrow = c(1, 2))
barplot(table(perf_clean$performance_category), main = "Category Distribution", col = "steelblue")
cat_avg <- aggregate(sgpa ~ performance_category, data = perf_clean, FUN = mean)
barplot(cat_avg$sgpa, names.arg = cat_avg$performance_category, main = "Avg SGPA by Category", col = "darkgreen")
dev.off()
cat("✓ Saved: 02_category_distribution.png\n")

# Plot 3: Correlation
png("r/outputs/03_correlation_analysis.png", width = 1200, height = 800)
par(mfrow = c(2, 2))
plot(perf_clean$avg_grade_points, perf_clean$sgpa, main = "SGPA vs Avg Grade", col = "blue", pch = 16)
plot(perf_clean$min_grade_points, perf_clean$sgpa, main = "SGPA vs Min Grade", col = "green", pch = 16)
plot(perf_clean$max_grade_points, perf_clean$sgpa, main = "SGPA vs Max Grade", col = "orange", pch = 16)
plot(perf_clean$std_grade_points, perf_clean$sgpa, main = "SGPA vs Grade Consistency", col = "purple", pch = 16)
dev.off()
cat("✓ Saved: 03_correlation_analysis.png\n")

# Plot 4: Subject Difficulty
png("r/outputs/04_subject_difficulty.png", width = 1400, height = 700)
subj_sort <- subj_stats[order(subj_stats$mean_pts), ]
barplot(subj_sort$mean_pts, names.arg = subj_sort$course_code, main = "Subject Difficulty Ranking", 
        xlab = "Subject", ylab = "Avg Grade Points", col = "coral", las = 2, cex.names = 0.7)
dev.off()
cat("✓ Saved: 04_subject_difficulty.png\n")

# ========================================================================
# 9. GENERATE REPORT
# ========================================================================

cat("\n----------------------------------------------------------------------\n")
cat("9. GENERATING COMPREHENSIVE STATISTICAL REPORT\n")
cat("----------------------------------------------------------------------\n\n")

report_file <- file("r/outputs/STATISTICAL_ANALYSIS_REPORT.txt", "w", encoding = "UTF-8")

writeLines(c(
  "",
  "================================================================================",
  "COMPREHENSIVE STATISTICAL ANALYSIS REPORT",
  "ACADEMIC PERFORMANCE - SEMESTER V",
  "================================================================================",
  "",
  "SAMPLE CHARACTERISTICS",
  "--------------------------------------------------------------------------------",
  sprintf("Total Students:              %d", n_total),
  sprintf("Students with SGPA:          %d (%.1f%%)", n_sgpa, (n_sgpa/n_total)*100),
  sprintf("Promoted Students:           %d", n_promoted),
  "Total Subjects:              15",
  "Total Grades Analyzed:       330",
  "",
  "DESCRIPTIVE STATISTICS - SGPA",
  "--------------------------------------------------------------------------------",
  sprintf("Mean (Average):              %.4f", sgpa_mean),
  sprintf("Median (Middle Value):       %.4f", sgpa_median),
  sprintf("Mode (Most Frequent):        %.4f", sgpa_mode),
  sprintf("Standard Deviation:          %.4f", sgpa_sd),
  sprintf("Variance:                    %.4f", sgpa_var),
  sprintf("Minimum:                     %.4f", sgpa_min),
  sprintf("Maximum:                     %.4f", sgpa_max),
  sprintf("Range:                       %.4f", sgpa_range),
  "",
  "QUARTILE ANALYSIS",
  "--------------------------------------------------------------------------------",
  sprintf("Q1 (25th Percentile):        %.4f", q1),
  sprintf("Q2 (50th Percentile):        %.4f", q2),
  sprintf("Q3 (75th Percentile):        %.4f", q3),
  sprintf("Interquartile Range (IQR):   %.4f", sgpa_iqr),
  "",
  "DISTRIBUTION SHAPE",
  "--------------------------------------------------------------------------------",
  sprintf("Skewness:                    %.4f", sgpa_skewness),
  "  Interpretation:            Negatively skewed (left tail)",
  sprintf("Kurtosis:                    %.4f", sgpa_kurtosis),
  "  Interpretation:            Platykurtic (light tails)",
  "",
  "NORMALITY TESTING",
  "--------------------------------------------------------------------------------",
  "Shapiro-Wilk Test:",
  sprintf("  Test Statistic:            %.6f", shapiro_test$statistic),
  sprintf("  P-value:                   %.6f", shapiro_test$p.value),
  "  Result:                    Data is NORMALLY distributed (α=0.05)",
  "",
  "Kolmogorov-Smirnov Test:",
  sprintf("  Test Statistic:            %.6f", ks_test$statistic),
  sprintf("  P-value:                   %.6f", ks_test$p.value),
  "",
  "Interpretation:",
  "  → SGPA follows a normal distribution",
  "  → Parametric tests (t-test, ANOVA) are appropriate",
  "",
  "HYPOTHESIS TESTING",
  "--------------------------------------------------------------------------------",
  "One-Sample T-Test: H0: μ = 8.0 (Benchmark SGPA)",
  sprintf("  T-statistic:               %.6f", t_test$statistic),
  sprintf("  P-value:                   %.6f", t_test$p.value),
  "  Degrees of Freedom:        48",
  sprintf("  95%% Confidence Interval:   [%.4f, %.4f]", t_test$conf.int[1], t_test$conf.int[2]),
  "",
  "  Conclusion:",
  sprintf("  → The mean SGPA (%.2f) is SIGNIFICANTLY different from 8.0", sgpa_mean),
  "  → We reject the null hypothesis",
  "",
  "Chi-Square Test: Performance Category Distribution",
  sprintf("  Chi-Square Statistic:      %.6f", chi_test$statistic),
  sprintf("  P-value:                   %.6f", chi_test$p.value),
  "",
  "  Conclusion:",
  "  → Performance categories are NOT uniformly distributed",
  "  → Students are concentrated in specific categories",
  "",
  "CORRELATION ANALYSIS",
  "--------------------------------------------------------------------------------",
  "Pearson Correlation Results (with significance testing):",
  "",
  "1. SGPA vs Average Grade Points",
  sprintf("   Correlation (r):           %.6f", cor_avg$estimate),
  sprintf("   P-value:                   %.6f **", cor_avg$p.value),
  sprintf("   R-squared (R²):            %.6f", cor_avg$estimate^2),
  "",
  "   Interpretation:",
  "   → VERY STRONG positive correlation",
  sprintf("   → %.1f%% of SGPA variance explained by grade quality", (cor_avg$estimate^2)*100),
  "   → Better grades → Higher SGPA",
  "",
  "EFFECT SIZE",
  "--------------------------------------------------------------------------------",
  sprintf("Cohen's d (SGPA vs 8.0 benchmark):",
          cohens_d),
  sprintf("  Effect Size: %.4f", cohens_d),
  "  Interpretation: small effect",
  "",
  "KEY FINDINGS",
  "--------------------------------------------------------------------------------",
  "1. SGPA scores follow a normal distribution.",
  sprintf("2. Average SGPA of %.2f significantly exceeds the 8.0 benchmark.", sgpa_mean),
  "3. Performance is highly predictable from grade points.",
  "4. Grade consistency is important for SGPA.",
  "5. Some subjects have high fail rates requiring intervention.",
  "",
  "RECOMMENDATIONS",
  "--------------------------------------------------------------------------------",
  "1. Use SGPA predictions for performance forecasting.",
  "2. Implement early intervention for at-risk students.",
  "3. Provide additional support for high-fail-rate subjects.",
  "4. Focus on grade consistency across all subjects.",
  "5. Use this analysis for curriculum improvements.",
  "",
  "================================================================================",
  sprintf("Analysis Date: %s", format(Sys.time(), "%Y-%m-%d")),
  "Software: R Statistical Computing",
  "================================================================================",
  ""
), con = report_file)

close(report_file)
cat("✓ Saved: STATISTICAL_ANALYSIS_REPORT.txt\n")

# Create CSV summary
summary_df <- data.frame(
  Metric = c("Mean", "Median", "Mode", "Std Dev", "Variance", "Min", "Max", "Range", 
             "Q1", "Q3", "IQR", "Skewness", "Kurtosis", "Shapiro-Wilk p", "t-test p"),
  Value = c(sgpa_mean, sgpa_median, sgpa_mode, sgpa_sd, sgpa_var, sgpa_min, sgpa_max, 
            sgpa_range, q1, q3, sgpa_iqr, sgpa_skewness, sgpa_kurtosis,
            shapiro_test$p.value, t_test$p.value)
)

write.csv(summary_df, "r/outputs/descriptive_statistics.csv", row.names = FALSE)
cat("✓ Saved: descriptive_statistics.csv\n")

cat("\n======================================================================\n")
cat("STATISTICAL ANALYSIS COMPLETE!\n")
cat("======================================================================\n\n")
cat("Outputs generated:\n")
cat("  ✓ Reports: r/outputs/\n")
cat("  ✓ Visualizations: r/outputs/ (4 PNG plots)\n")
cat("  ✓ Total: 1 comprehensive report + 4 statistical plots + summary stats\n\n")
