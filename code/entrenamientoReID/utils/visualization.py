import torchreid

def visualize_results(model_path, dataset_dir):
    model = build_model(1)
    model.load_state_dict(torch.load(model_path))
    model.eval()
    
    datamanager = get_datamanager(dataset_dir)
    
    distmat, q_pids, g_pids, q_camids, g_camids = torchreid.utils.feature_extraction(
        model,
        datamanager.test_loader,
        datamanager.test_loader,
        use_gpu=True
    )
    
    cmc, mAP = torchreid.utils.eval_rank(
        distmat,
        q_pids,
        g_pids,
        q_camids,
        g_camids
    )
    
    print(f"mAP: {mAP:.1%}")
    print(f"CMC top-1: {cmc[0]:.1%}")
    print(f"CMC top-5: {cmc[4]:.1%}")
    
    torchreid.utils.visualize_rank(
        distmat,
        datamanager.test_loader,
        datamanager.test_loader,
        save_dir='visrank_results',
        topk=5
    )