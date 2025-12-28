# solution.py
import sys

def get_solve_case():
    def solve_case(tc, it):
        try:
            line = next(it)
            N = int(line)
            M = int(next(it))
            A = int(next(it))
            B = int(next(it))
        except StopIteration:
            return False
            
        ids_by_res = [[] for _ in range(M)]
        total_v = 0
        total_s = 0
        
        for i in range(1, N + 1):
            for j in range(1, M + 2):
                w = int(next(it))
                if w != -1:
                    r = w % M
                    rid = (i - 1) * (M + 1) + j
                    ids_by_res[r].append(rid)
                    total_v += 1
                    total_s = (total_s + r) % M
        
        # We care about excluding e items such that e < 2M
        limit_e = min(total_v, 2 * M - 1)
        mask = (1 << M) - 1
        
        # DP state: dp[size] = bitset of sums
        dp = [0] * (limit_e + 1)
        dp[0] = 1
        
        snapshots = [0] * M
        meta_items = [[] for _ in range(M)]
        
        counts = [len(ids_by_res[r]) for r in range(M)]
        
        # Non-zero items first
        for r in range(1, M):
            c = counts[r]
            if c > 0:
                curr = 1
                while c > 0:
                    take = min(c, curr)
                    r_sum = (take * r) % M
                    meta_items[r].append((take, r_sum))
                    for i in range(limit_e, take - 1, -1):
                        if dp[i-take]:
                            shifted = ((dp[i-take] << r_sum) | (dp[i-take] >> (M-r_sum))) & mask
                            dp[i] |= shifted
                    c -= take
                    curr *= 2
            snapshots[r] = list(dp)
            
        # Zeros
        n0 = counts[0]
        dp_final = list(dp)
        # Note: zeros only change the size, not the sum.
        # But for reconstruction we need to know how many zeros were used.
        # Let's just calculate dp_final as the union of shifted dp
        for z in range(1, min(limit_e, n0) + 1):
            for i in range(limit_e, z-1, -1):
                dp_final[i] |= dp[i-z]
        
        best_eff = -1
        best_K = 0
        best_E = 0
        best_s_ex = 0
        
        for K in range((total_v // M) + 1):
            E = total_v - K * M
            if E < 0 or E > limit_e: continue
            
            b = dp_final[E]
            if b == 0: continue
            
            for s in range(M):
                if (b >> s) & 1:
                    penalty = (total_s - s) % M
                    eff = K * A - B * penalty
                    if eff >= best_eff:
                        best_eff = eff
                        best_K = K
                        best_E = E
                        best_s_ex = s
        
        # Output
        out_buf = get_output_buffer()
        out_buf.write(f"Case #{tc}: {best_eff} {best_K}\n".encode())
        if best_K == 0:
            return True
            
        # Reconstruct
        # Find nz needed such that dp[nz] has correct s
        best_nz = -1
        for nz in range(limit_e + 1):
            n0_used = best_E - nz
            if 0 <= n0_used <= n0:
                if (dp[nz] >> best_s_ex) & 1:
                    best_nz = nz
                    break
        
        # Exclude IDs
        used_for_teams = [[] for _ in range(M)]
        for r in range(1, M):
            used_for_teams[r] = list(ids_by_res[r])
        used_for_teams[0] = list(ids_by_res[0])
        
        def pick_id(r):
            return used_for_teams[r].pop()
            
        # Exclude best_E items
        curr_n = best_nz
        curr_s = best_s_ex
        for _ in range(best_E - best_nz):
            pick_id(0)
            
        for r in range(M-1, 0, -1):
            if not meta_items[r]: continue
            prev_base = snapshots[r-1] if r > 1 else ([1] + [0]*limit_e)
            
            states = [list(prev_base)]
            for s_sz, r_sm in meta_items[r]:
                prev = states[-1]
                nex = list(prev)
                for i in range(limit_e, s_sz-1, -1):
                    if prev[i-s_sz]:
                        shifted = ((prev[i-s_sz] << r_sm) | (prev[i-s_sz] >> (M-r_sm))) & mask
                        nex[i] |= shifted
                states.append(nex)
                
            for m_idx in range(len(meta_items[r])-1, -1, -1):
                s_sz, r_sm = meta_items[r][m_idx]
                prev_st = states[m_idx]
                prev_s = (curr_s - r_sm) % M
                if curr_n >= s_sz and (prev_st[curr_n-s_sz] >> prev_s) & 1:
                    for _ in range(s_sz):
                        pick_id(r)
                    curr_n -= s_sz
                    curr_s = prev_s
                    
        # Items remaining in used_for_teams are for the best_K teams
        rem_items = []
        for r in range(M):
            for rid in used_for_teams[r]:
                rem_items.append((rid, r))
                
        # Partition into teams
        while len(rem_items) >= M:
            if len(rem_items) >= 2*M - 1:
                dp_egz = [0]*(M+1)
                dp_egz[0] = 1
                states = [list(dp_egz)]
                for i in range(len(rem_items)):
                    r = rem_items[i][1]
                    prev = states[-1]
                    nxt = list(prev)
                    for c in range(M, 0, -1):
                        if prev[c-1]:
                            shifted = ((prev[c-1] << r) | (prev[c-1] >> (M-r))) & mask
                            nxt[c] |= shifted
                    states.append(nxt)
                
                team = []
                cc = M
                cs = 0
                new_rem = []
                for i in range(len(rem_items)-1, -1, -1):
                    rid, r = rem_items[i]
                    if cc > 0:
                        ps = (cs - r) % M
                        if (states[i][cc-1] >> ps) & 1:
                            team.append(rid)
                            cc -= 1
                            cs = ps
                            continue
                    new_rem.append((rid, r))
                out_buf.write((" ".join(map(str, team)) + "\n").encode())
                rem_items = new_rem[::-1]
            else:
                out_buf.write((" ".join(map(str, [x[0] for x in rem_items])) + "\n").encode())
                rem_items = []
        return True

    return solve_case

def get_input_buffer():
    if hasattr(sys.stdin, 'buffer'):
        return sys.stdin.buffer
    return sys.stdin

def get_output_buffer():
    if hasattr(sys.stdout, 'buffer'):
        return sys.stdout.buffer
    return sys.stdout

def main():
    data = get_input_buffer().read().split()
    if not data: return
    it = iter(data)
    T_cases = int(next(it))
    solve_case = get_solve_case()
    for tc in range(1, T_cases + 1):
        if not solve_case(tc, it): break

if __name__ == "__main__":
    import io
    try:
        with open("input.txt", "rb") as f_in:
            with open("output.txt", "wb") as f_out:
                # Mock buffer for file objects
                class MockSys:
                    def __init__(self, stdin, stdout):
                        self.stdin = stdin
                        self.stdout = stdout
                
                # Actually, the simplest way is to change the main to use sys.stdin directly if buffer is missing
                # But let's just make main take optional streams
                sys.stdin = f_in
                sys.stdout = f_out
                main()
    except FileNotFoundError:
        main()