library("jsonlite")
library("DESeq2")
library("tximport")

args <- commandArgs(trailingOnly = TRUE)
data1 <- args[1]
data2 <- args[2]
output_path <- args[3]

data_1_v <- fromJSON(data1)
data_2_v <- fromJSON(data2)
files <- c(data_1_v, data_2_v)
num_samples <- length(data_1_v)

for (file in data_1_v) {
  print(file)
}
# conditions <- c(rep("Group1", num_samples), rep("Group2", num_samples))
# for (i in 1:num_samples) {
#   group_1 <- c(group_1, paste("Group1_sample", i))
# }
# for (i in 1:num_samples) {
#   group_2 <- c(group_2, paste("Group2_sample", i))
# }

# samples <- data.frame("run" = c(group_1, group_2), "condition"  = conditions)
# names(files) <- samples$run

# txi <- tximport(files, type="rsem")
# txi$length[txi$length == 0] <- 1
# ddsTxi <- DESeqDataSetFromTximport(txi,
#                                    colData = samples,
#                                    design = ~ condition)

# # TODO
# smallestGroupSize <- 3
# keep <- rowSums(counts(ddsTxi) >= 10) >= smallestGroupSize
# ddsTxi <- ddsTxi[keep,]
# ddsTxi <- DESeq(ddsTxi)
# df <- results(ddsTxi)
# df$diffexpressed <- "NO"
# df$diffexpressed[df$log2FoldChange > 0 & df$padj < 0.05] <- "UP"
# df$diffexpressed[df$log2FoldChange < 0 & df$padj < 0.05] <- "DOWN"
# df$delabel <- ifelse(df$X %in% head(df[order(df$padj), "X"], 30), df$X, NA)

# p <-ggplot(data = df, aes(x = log2FoldChange, y = -log10(padj), col = diffexpressed, label = delabel)) +
#   geom_vline(xintercept = 0, col = "gray", linetype = 'dashed') +
#   geom_hline(yintercept = -log10(0.05), col = "gray", linetype = 'dashed') + 
#   geom_point(size = 1) + 
#   scale_color_manual(values = c("#00AFBB", "grey", "#bb0c00"), # to set the colours of our variable  
#                      labels = c("Downregulated", "Not significant", "Upregulated")) + # to set the labels in case we want to overwrite the categories from the dataframe (UP, DOWN, NO)
#   coord_cartesian(ylim = c(0, 50), xlim = c(-10, 10)) + # since some genes can have minuslog10padj of inf, we set these limits
#   labs(color = 'Severe', #legend_title, 
#        x = expression("log"[2]*"FoldChange"), y = expression("-log"[10]*"p-value")) + 
#   scale_x_continuous(breaks = seq(-10, 10, 2)) + # to customise the breaks in the x axis
#   ggtitle('volcano plot--ddsTxi result') + 
#   geom_text() 