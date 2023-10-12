# The packages can be installed within R with:
# intstall.packages(c("tidyverse", "ggrepel"))

# Load packages
library(tidyverse)
library(ggrepel)


# options #

options(ggrepel.max.overlaps = Inf)

# set working directory #
setwd(dirname(rstudioapi::getActiveDocumentContext()$path))

# Folders #

Folder1 <- "Data/Plot data/Volcano/TEST"
Folder2 <- "Results/Volcano/Images/TEST"
Folder3 <- "Results/Volcano/Data/TEST"

dir.create(file.path(Folder2),recursive = TRUE, showWarnings = FALSE)
dir.create(file.path(Folder3),recursive = TRUE, showWarnings = FALSE)

# Files #

File1 = "Overview table.csv"
File2 = "Volcano_plot_Control_to_iNPH_Grouped.png"
File3 = "Volcano_plot_Control_to_iNPH_Grouped_labeled.png"
File4 = "Significant_compounds.csv"
File5 = "Significant_compounds_group_out_over_3_log2FC.csv"

File6 = "Volcano_plot_Control_to_SAH_Grouped_Log2FC_above3.png"
File7 = "Volcano_plot_Control_to_SAH_Grouped_Log2FC_above3_labeled.png"

## Read data ##

data <- read.table(file.path(Folder1, File1),header=T, sep=";",stringsAsFactors=T)

#data$Padj2 <- p.adjust(data$Pvalue,method="BH")

data <- data %>% 
  mutate(
    Expression = case_when(Log2FC >= 0 & Padj <= 0.05 ~ "Up-regulated",
                           Log2FC < 0 & Padj <= 0.05 ~ "Down-regulated",
                           TRUE ~ "Unchanged")
  )


# Find differentially expressed genes #

top <- 100
top_genes <- bind_rows(
  data %>% 
    filter(Expression == 'Up-regulated') %>% 
    arrange(Padj, desc(abs(Log2FC))) %>% 
    head(top),
  data %>% 
    filter(Expression == 'Down-regulated') %>% 
    arrange(Padj, desc(abs(Log2FC))) %>% 
    head(top)
)

data$top_genes <- ifelse(data$Compounds %in% top_genes$Compounds, 1, 0)
data <- data %>% 
  mutate(
    Expression_top = case_when(top_genes == 1 & Expression == "Up-regulated" ~ "Up-regulated",
                               top_genes == 1 & Expression == "Down-regulated" ~ "Down-regulated",
                               TRUE ~ "Unchanged")
  )

#write.csv2(top_genes,file.path(Folder3, "Significant_pvalues.csv"), row.names = FALSE)

Order_list = c("Amides",
               "Ceramides",
               "Cholesteryl esters",
               "Fatty acids",
               "Lysophosphatidylcholines",
               "Monoacrylglycerols",
               "Phosphatidic acids",
               "Phosphatidylcholines",
               "Phosphatidylethanolamines",
               "Phosphatidylserines",
               "Phosphocholines",
               "Plasmenylphosphatidylcholines",
               "Plasmenylphosphatidylethaolamines",
               "Platelet-activating factors",
               "Sphingomyelines",
               "Triacylglycerols",
               "Small group collection",
               "Others")

Order_list_color = c("#9BC2E6",
  "#4F93D1",
  "#00B0F0",
  "#BF8F00",
  "#99FF33",
  "#92D050",
  "#597319",
  "#00B050",
  "#993366",
  "#FF6699",
  "#E25D60",
  "#00FF99",
  "#A31D20",
  "#FF0000",
  "#FF9900",
  "#7030A0",
  "#CC00CC",
  "#FFFFFF")


# p1 <- ggplot(data %>%
#                arrange(match(Groups, rev(Order_list))),
#                        aes(Log2FC , -log(Pvalue,10))) +
#   geom_vline(xintercept=c(0.0),linetype = "dashed" ,col="grey50") +
#   geom_hline(yintercept=-log10(0.05),linetype = "dashed", col="grey50")+
#   geom_point(aes(fill = Expression), size = 4,shape=21)+
#   scale_x_continuous(name=expression("log"[2]*"FC"))+
#   ylab(expression("-log"[10]*"pvalue")) +
#   scale_fill_manual(values = c("dodgerblue3", "gray80", "firebrick3")) +
#   #guides(colour = guide_legend(override.aes = list(size=1)))+
#   #scale_fill_manual(breaks=Order_list,values=Order_list_color)+
#   theme_classic()
# p1

p1 <- ggplot(data %>%
               arrange(match(Groups, rev(Order_list))),
             aes(Log2FC , -log(Pvalue,10))) +
  geom_vline(xintercept=c(0),linetype = "dashed" ,col="grey50") +
  geom_hline(yintercept=-log10(0.05),linetype = "dashed", col="grey50")+
  geom_hline(yintercept=-log10(7.838308e-03),linetype = "dashed", col="grey50")+
  geom_point(aes(fill = Groups), size = 4,shape=21)+
  scale_x_continuous(name=expression("log"[2]*"FC"))+
  ylab(expression("-log"[10]*"pvalue")) +
  #scale_fill_manual(values = c("dodgerblue3", "gray80", "firebrick3")) +
  #guides(colour = guide_legend(override.aes = list(size=1)))+
  scale_fill_manual(breaks=Order_list,values=Order_list_color)+
  theme_classic()
p1

ggsave(file=file.path(Folder2, File2),plot=p1,width = 14, height = 8,units = "in", bg = "transparent",dpi=1200)



p2 <-  p1 +
  geom_label_repel(data = top_genes,
                   mapping = aes(Log2FC, -log(Pvalue,10), label = Compounds),
                   size = 2)+theme(legend.position="none")
p2
ggsave(file=file.path(Folder2, File3),plot=p2,width = 14, height = 8,units = "in", bg = "transparent",dpi=1200)

# png(filename = file.path(Folder1, File3),
#     width = 12, height = 8, units = "in",
#     bg = "transparent",res=1600)
# p2
# dev.off()

write.csv2(data,file.path(Folder3, File4), row.names = FALSE)
