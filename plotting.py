import torch
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import LogNorm
from torch_geometric.data import Batch

def run_prediction_prompt(loaded_models, plotting_examples, example_metadata, periods_to_plot, device):
    #Mapping period values to their index
    period_map = {val: (idx, label) for val, idx, label in periods_to_plot}

    print("=== Model Prediction Setup ===")
    
    #1. Model
    valid_models = list(loaded_models.keys())
    print(f"Available models: {valid_models}")
    model_name = input("Type the name of the model you want to use: ").strip()
    
    if model_name not in loaded_models:
        print(f"\n[!] Error: '{model_name}' is not recognized. Please run the cell again and type a valid name.")
        return

    #2. Example
    print("\nAvailable examples:")
    for i, meta in enumerate(example_metadata):
        print(f"  [{i}] {meta['source_info']}")
        
    try:
        example_idx = int(input("\nType the number (0-9) of the example you want to visualize: ").strip())
        if example_idx < 0 or example_idx >= len(example_metadata):
            raise ValueError
    except ValueError:
        print("\n[!] Error: Please enter integer from the list above. Please run the cell again.")
        return

    #3. Period
    valid_periods = list(period_map.keys())
    print(f"\nAvailable periods (s): {valid_periods}")
    try:
        period_val = float(input("Type the period you want to plot: ").strip())
        if period_val not in valid_periods:
            raise ValueError
    except ValueError:
        print("\n[!] Error: Please enter one of the exact period values listed above. Please run the cell again.")
        return
        
    #4. Saving png
    save_choice = input("\nWould you like to save this figure as a PNG? (y/n): ").strip().lower()

    #5. Generate
    print(f"\nGenerating plot for Model: {model_name.upper()} | Example: {example_idx} | Period: {period_val}s...")

    #Load in chosen model
    model = loaded_models[model_name]
    model.eval()

    #grab one of the 10 examples and associated data
    example_graph = plotting_examples[example_idx]
    meta = example_metadata[example_idx]
    period_idx, period_label = period_map[period_val]
    
    #Create a batch and get model prediction
    example_batch = Batch.from_data_list([example_graph]).to(device)
    with torch.no_grad():
        predictions = model(example_batch)
    
    #Move data to CPU and convert to NumPy
    pos = example_graph.pos_plot.cpu().numpy() #lat and lon values of sites
    ground_truth = example_graph.y.cpu().numpy() #CyberShake-GMMs training target
    predictions = predictions.cpu().numpy() #GNN prediction
    mean = example_graph.gmm_mean.cpu().numpy() #GMMs prediction

    #Calculate SA values
    full_ground_truth = ground_truth + mean #Add back the mean of the GMMs to GNN prediction
    full_predictions = predictions + mean #Add back the mean of the GMMs to CyberShake prediction
    mean_SA = np.exp(mean) #Changing the values to linear to plot it in log-space
    full_ground_truth_SA = np.exp(full_ground_truth) #Changing the values to linear to plot it in log-space
    full_predictions_SA = np.exp(full_predictions) #Changing the values to linear to plot it in log-space

    #Slice Data for the specific period
    cyber = full_ground_truth_SA[:, period_idx]
    gnn_preds = full_predictions_SA[:, period_idx]
    gmm_mean = mean_SA[:, period_idx]

    #Calculate differences
    res_1 = full_ground_truth[:, period_idx] - full_predictions[:, period_idx] 
    res_2 = full_ground_truth[:, period_idx] - mean[:, period_idx]             
    res_3 = full_predictions[:, period_idx] - mean[:, period_idx]             

    #Create plot
    fig, axes = plt.subplots(2, 3, figsize=(18, 8), sharey=True, constrained_layout=True)
    axes = axes.flatten()

    log_norm = LogNorm(vmin=cyber.min(), vmax=cyber.max())
    res_norm = plt.Normalize(vmin=-1.5, vmax=1.5)

    #Surface fault trace and hypocenter
    for ax in axes:
        ax.plot(meta["fault_lon"], meta["fault_lat"], color='black', linewidth=1, zorder=3)
        ax.plot(meta["event_lon"], meta["event_lat"], marker='*', color='red', markersize=15, zorder=3)
        ax.grid(True)
        
    #Top Row: SA Values
    scatter1 = axes[0].scatter(pos[:, 0], pos[:, 1], c=cyber, cmap='viridis', norm=log_norm, s=100)
    axes[0].set_title('CyberShake Spectral Acceleration')
    axes[0].set_ylabel('Latitude')
    
    axes[1].scatter(pos[:, 0], pos[:, 1], c=gnn_preds, cmap='viridis', norm=log_norm, s=100)
    axes[1].set_title('GNN Predicted Spectral Acceleration')
    
    axes[2].scatter(pos[:, 0], pos[:, 1], c=gmm_mean, cmap='viridis', norm=log_norm, s=100)
    axes[2].set_title('GMMs (mean) Spectral Acceleration')
    
    #Bottom Row: Differences
    scatter4 = axes[3].scatter(pos[:, 0], pos[:, 1], c=res_1, cmap='BrBG', norm=res_norm, s=100, edgecolors='black')
    axes[3].set_title('CyberShake - GNN')
    axes[3].set_xlabel('Longitude')
    axes[3].set_ylabel('Latitude')

    axes[4].scatter(pos[:, 0], pos[:, 1], c=res_2, cmap='BrBG', norm=res_norm, s=100, edgecolors='black')
    axes[4].set_title('CyberShake - GMMs (mean)')
    axes[4].set_xlabel('Longitude')
    
    axes[5].scatter(pos[:, 0], pos[:, 1], c=res_3, cmap='BrBG', norm=res_norm, s=100, edgecolors='black')
    axes[5].set_title('GNN - GMMs (mean)')
    axes[5].set_xlabel('Longitude')

    #Mean and Std for differences 
    res_list = [(res_1, axes[3]), (res_2, axes[4]), (res_3, axes[5])]

    for res_data, ax in res_list:
        mu = np.mean(res_data)
        std = np.std(res_data)
        stats_text = f"$\\mu$: {mu:.3f}\n$\\sigma$: {std:.3f}"
        
        ax.text(0.05, 0.05, stats_text, transform=ax.transAxes,
                verticalalignment='bottom', fontsize=11, fontweight='bold',
                bbox=dict(boxstyle='round', facecolor='white', alpha=0.8))
        
    #Colorbars and Labels
    fig.colorbar(scatter1, ax=axes[0:3], location='right', label='SA (g)')
    fig.colorbar(scatter4, ax=axes[3:6], location='right', label='ln Difference')
    fig.suptitle(f'Model: {model_name.upper()} | Source: {meta["source_info"]} | Period = {period_val}s', fontsize=14)

    #Saving PNG
    if save_choice in ['y', 'yes']:
        
        filename = f"{model_name}_example{example_idx}_{period_label}.png"
        
        plt.savefig(filename, dpi=300, bbox_inches='tight')
        print(f"\nSaved as: {filename}")

    #Show the plot
    plt.show()