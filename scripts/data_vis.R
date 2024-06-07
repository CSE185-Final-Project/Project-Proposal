cat("Start to install necessary packages\n")
silent_install <- function(pkg) {
  if (!require(pkg, character.only = TRUE)) {
    suppressMessages(suppressWarnings(install.packages(pkg, quiet = TRUE)))
    suppressMessages(suppressWarnings(library(pkg, character.only = TRUE)))
  }
}
silent_install("jsonlite")
silent_install("DESeq2")
silent_install("tximport")
silent_install("ggplot2")
library("jsonlite")
library("DESeq2")
library("tximport")
library("ggplot2")

cat("Finish installing\n")

args <- commandArgs(trailingOnly = TRUE)

data1 <- args[1]
data2 <- args[2]

output_path <- args[3]
output_path <- trimws(output_path)

p_value <- as.numeric(args[4])

fod <- as.numeric(args[5])
fod <- log2(fod)

filter <- as.numeric(args[6])

name <- args[7]
name <- trimws(name)

deseq2 <- args[8]

data_1_v <- fromJSON(data1)
data_2_v <- fromJSON(data2)
files <- c(data_1_v, data_2_v)
num_samples_1 <- length(data_1_v)
num_samples_2 <- length(data_1_v)
smallestGroupSize <- min(c(num_samples_1, num_samples_2))

group_1 <- c()
group_2 <- c()
conditions <- c(rep("Group1", num_samples_1), rep("Group2", num_samples_2))
for (i in 1:num_samples_1) {
  group_1 <- c(group_1, paste("Group1_sample", i))
}
for (i in 1:num_samples_2) {
  group_2 <- c(group_2, paste("Group2_sample", i))
}

samples <- data.frame("run" = c(group_1, group_2), "condition"  = conditions)
names(files) <- samples$run


txi <- tximport(files, type = "rsem")
txi$length[txi$length == 0] <- 1
ddsTxi <- DESeqDataSetFromTximport(txi,
                                   colData = samples,
                                   design = ~ condition)

keep <- rowSums(counts(ddsTxi) >= filter) >= smallestGroupSize
ddsTxi <- ddsTxi[keep,]
ddsTxi <- DESeq(ddsTxi)
df <- results(ddsTxi)
df <- as.data.frame(df)
write.csv(df, file = paste0(output_path, "/result_deseq2.csv"), row.names = TRUE)
if (deseq2 == "True") {
  cat("Visualization is skipped because -d is present\n")
  quit()
}
df$diffexpressed <- "NO"
df$diffexpressed[df$log2FoldChange > fod & df$padj < p_value] <- "UP"
df$diffexpressed[df$log2FoldChange < -fod & df$padj < p_value] <- "DOWN"
df$X <- row.names(df)
if (name == "NO") {
  top_30_names <- head(df[order(df$padj), "X"], 30)
  df$delabel <- ifelse(df$X %in% top_30_names & df$diffexpressed != "NO", df$X, NA)
} else {
  df_name <- read.csv(name, header = FALSE, sep = "\t")
  colnames(df_name) <- c("X", "Name")
  df <- merge(df, df_name, by = "X", all.x = TRUE)
  top_30_names <- head(df[order(df$padj), "Name"], 30)
  df$delabel <- ifelse(df$Name %in% top_30_names & df$diffexpressed != "NO", df$Name, NA)
}
p <-ggplot(data = df, aes(x = log2FoldChange, y = -log10(padj), col = diffexpressed, label = delabel)) +
  geom_vline(xintercept = -fod, col = "gray", linetype = 'dashed') +
  geom_vline(xintercept = fod, col = "gray", linetype = 'dashed') +
  geom_hline(yintercept = -log10(p_value), col = "gray", linetype = 'dashed') + 
  geom_point(size = 1) + 
  scale_color_manual(values = c("#00AFBB", "grey", "#bb0c00"),
                     labels = c("Downregulated", "Not significant", "Upregulated")) +
  coord_cartesian(ylim = c(0, 50), xlim = c(-10, 10)) + 
  labs(color = 'Severe', #legend_title,
       x = expression("log"[2]*"FoldChange"), y = expression("-log"[10]*"p-value")) + 
  scale_x_continuous(breaks = seq(-10, 10, 2)) +
  ggtitle("volcano plot--ddsTxi result") +
  geom_text() 
ggsave(paste0(output_path, "/result_vol_plot.png", collapse = NULL), plot = p, width = 8, height = 6, units = "in")
