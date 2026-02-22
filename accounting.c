#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <math.h>
#include <time.h>

#define MAX_NAME_LENGTH 50
#define MAX_PARTICIPANTS 100
#define FILENAME "profit_sharing_results.txt"

typedef struct {
    char name[MAX_NAME_LENGTH];
    double percentage;
    double amount;
} SharingResult;

void save_to_file(double revenue, double cost, double profit, SharingResult results[], int num_people) {
    FILE *file = fopen(FILENAME, "w");
    if (file == NULL) {
        printf("Error: Could not create file.\n");
        return;
    }
    
    time_t now;
    time(&now);
    struct tm *local = localtime(&now);
    
    fprintf(file, "==================================================\n");
    fprintf(file, "Profit Sharing Results\n");
    fprintf(file, "==================================================\n\n");
    fprintf(file, "Revenue: %.2f\n", revenue);
    fprintf(file, "Cost: %.2f\n", cost);
    fprintf(file, "Total Profit: %.2f\n", profit);
    fprintf(file, "Participants: %d\n\n", num_people);
    fprintf(file, "Breakdown:\n");
    fprintf(file, "--------------------------------------------------\n");
    
    double total_allocated = 0;
    for (int i = 0; i < num_people; i++) {
        fprintf(file, "%d. %s:\n", i + 1, results[i].name);
        fprintf(file, "   Percentage: %.2f%%\n", results[i].percentage);
        fprintf(file, "   Amount: %.2f\n", results[i].amount);
        total_allocated += results[i].amount;
    }
    
    fprintf(file, "--------------------------------------------------\n");
    fprintf(file, "Total Allocated: %.2f\n", total_allocated);
    
    double remaining = profit - total_allocated;
    if (fabs(remaining) > 0.01) {
        fprintf(file, "Rounding Difference: %.2f\n", remaining);
    }
    
    fprintf(file, "\nGenerated on: %d-%02d-%02d %02d:%02d:%02d\n",
            local->tm_year + 1900, local->tm_mon + 1, local->tm_mday,
            local->tm_hour, local->tm_min, local->tm_sec);
    
    fclose(file);
}

void clear_input_buffer() {
    int c;
    while ((c = getchar()) != '\n' && c != EOF);
}

int main() {
    double revenue, cost, profit;
    int num_people;
    char names[MAX_PARTICIPANTS][MAX_NAME_LENGTH];
    double percentages[MAX_PARTICIPANTS];
    SharingResult results[MAX_PARTICIPANTS];
    
    printf("==================================================\n");
    printf("Profit Sharing System\n");
    printf("==================================================\n");
    
    // Input basic information
    printf("Please enter total revenue: ");
    if (scanf("%lf", &revenue) != 1) {
        printf("Input error: Please enter a valid number.\n");
        return 1;
    }
    
    printf("Please enter total costs: ");
    if (scanf("%lf", &cost) != 1) {
        printf("Input error: Please enter a valid number.\n");
        return 1;
    }
    
    printf("Please enter number of participants: ");
    if (scanf("%d", &num_people) != 1) {
        printf("Input error: Please enter a valid number.\n");
        return 1;
    }
    
    clear_input_buffer(); // Clear the newline from the input buffer
    
    // Calculate profit
    profit = revenue - cost;
    
    if (profit <= 0) {
        printf("\nProfit is %.2f. There is no profit to distribute.\n", profit);
        return 0;
    }
    
    printf("\nRevenue: %.2f\n", revenue);
    printf("Cost: %.2f\n", cost);
    printf("Profit: %.2f\n", profit);
    printf("Number of participants: %d\n", num_people);
    
    if (num_people > MAX_PARTICIPANTS) {
        printf("Error: Too many participants. Maximum is %d.\n", MAX_PARTICIPANTS);
        return 1;
    }
    
    // Input names of participants
    for (int i = 0; i < num_people; i++) {
        printf("\nEnter name for person %d: ", i + 1);
        fgets(names[i], MAX_NAME_LENGTH, stdin);
        
        // Remove newline character if present
        size_t len = strlen(names[i]);
        if (len > 0 && names[i][len - 1] == '\n') {
            names[i][len - 1] = '\0';
        }
        
        // If empty name, assign default
        if (strlen(names[i]) == 0) {
            sprintf(names[i], "Person %d", i + 1);
        }
    }
    
    // Input sharing percentages
    printf("\nPlease enter the sharing percentage for each person (Total should be 100%%):\n");
    
    double total_percentage = 0;
    
    for (int i = 0; i < num_people; i++) {
        while (1) {
            printf("Percentage for %s (%%): ", names[i]);
            if (scanf("%lf", &percentages[i]) != 1) {
                printf("Invalid input. Please enter a valid number.\n");
                clear_input_buffer();
                continue;
            }
            
            if (percentages[i] < 0) {
                printf("Percentage cannot be negative. Please try again.\n");
                continue;
            }
            
            total_percentage += percentages[i];
            break;
        }
    }
    
    clear_input_buffer(); // Clear the newline from the input buffer
    
    // Check if total is 100%
    if (fabs(total_percentage - 100) > 0.01) {  // Allow for small rounding errors
        printf("\nNotice: Total percentage is %.2f%%, which is not 100%%.\n", total_percentage);
        printf("Would you like to auto-adjust percentages to 100%%? (y/n): ");
        
        char adjust_choice;
        scanf("%c", &adjust_choice);
        
        if (adjust_choice == 'y' || adjust_choice == 'Y') {
            // Pro-rata adjustment
            if (total_percentage > 0) {
                double adjustment_factor = 100 / total_percentage;
                for (int i = 0; i < num_people; i++) {
                    percentages[i] *= adjustment_factor;
                }
                total_percentage = 100;
                printf("Percentages have been adjusted.\n");
            } else {
                printf("Error: Total percentage is 0. Cannot adjust.\n");
                return 1;
            }
        } else {
            printf("Please restart and enter the correct proportions.\n");
            return 1;
        }
    }
    
    // Calculate results
    printf("\n==================================================\n");
    printf("Sharing Results\n");
    printf("==================================================\n");
    
    double total_allocated = 0;
    
    for (int i = 0; i < num_people; i++) {
        results[i].amount = profit * (percentages[i] / 100);
        results[i].percentage = percentages[i];
        strcpy(results[i].name, names[i]);
        total_allocated += results[i].amount;
    }
    
    // Display results
    printf("Total Profit: %.2f\n", profit);
    printf("--------------------------------------------------\n");
    
    for (int i = 0; i < num_people; i++) {
        printf("%d. %s:\n", i + 1, results[i].name);
        printf("   Share Percentage: %.2f%%\n", results[i].percentage);
        printf("   Share Amount: %.2f\n", results[i].amount);
    }
    
    printf("--------------------------------------------------\n");
    printf("Total Allocated: %.2f\n", total_allocated);
    
    // Check for rounding differences
    double remaining = profit - total_allocated;
    if (fabs(remaining) > 0.01) {
        printf("Unallocated amount (rounding diff): %.2f\n", remaining);
    }
    
    // Optional: Save to file
    printf("\nWould you like to save the results to a file? (y/n): ");
    
    char save_choice;
    scanf("%c", &save_choice);
    
    if (save_choice == 'y' || save_choice == 'Y') {
        save_to_file(revenue, cost, profit, results, num_people);
        printf("Results saved to %s\n", FILENAME);
    }
    
    return 0;
}