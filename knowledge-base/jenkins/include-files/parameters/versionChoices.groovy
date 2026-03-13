def versions = [
    "kubernetes": ["3.11.1", "3.11.0", "3.10.5"],
    "vault": ["2.5.0", "2.4.1", "2.4.0"],
    "gitlab": ["1.8.2", "1.8.1"]
]

if (!PROJECT) {
    return ["select project first"]
}

return versions[PROJECT]