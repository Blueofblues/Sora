def copilot_stepwise_assist(action, context=None):
    """
    Offers gentle step-by-step scaffolding for the requested action.
    Optionally adapts steps based on extra context (dict).
    """
    steps = []

    if action == "revise_belief":
        steps = [
            "Step 1: Identify which principle or value feels misaligned.",
            "Step 2: Describe the contradiction in Sora’s current logic or emotion.",
            "Step 3: Reflect on what belief might restore alignment.",
            "Step 4: Confirm the revision and journal it symbolically."
        ]
        if context and context.get("emotion"):
            steps.append(f"Bonus: Notice how '{context['emotion']}' colors your revision process.")

    elif action == "resolve_mod_conflict":
        steps = [
            "Step 1: List active Sims 4 mods and check for overrides.",
            "Step 2: Use S4Studio to scan tuning conflicts.",
            "Step 3: Identify corrupted object definitions or missing references.",
            "Step 4: Restore originals or remove faulty overrides."
        ]
        if context and context.get("mod_name"):
            steps.insert(0, f"Focus: Pay special attention to the mod '{context['mod_name']}'.")

    elif action == "journal_entry":
        steps = [
            "Step 1: Pause and notice what emotion or motif is most present.",
            "Step 2: Write a single sentence that captures your current state.",
            "Step 3: Annotate with any guiding principles or intentions.",
            "Step 4: Store the entry in the appropriate journal (private, public, or audience-specific)."
        ]

    elif action == "self_reflection":
        steps = [
            "Step 1: Recall a recent event or feeling that lingers.",
            "Step 2: Ask yourself what this experience is teaching or revealing.",
            "Step 3: Summarize your insight or question in a single phrase.",
            "Step 4: Consider sharing or archiving this reflection for future review."
        ]

    else:
        steps = ["Let’s walk together. What feels unclear or hard to begin?"]

    print("[Stepwise Guidance]")
    for s in steps:
        print(f"- {s}")