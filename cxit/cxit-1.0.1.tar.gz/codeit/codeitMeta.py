#Default template
def template_cp():
    template = """#include <bits/stdc++.h> 

using namespace std; 

int main() 
{ 
    ios_base::sync_with_stdio(false); 
    cin.tie(NULL); 

    /* This is needed as most contests use this format */
    #ifndef ONLINE_JUDGE  
        freopen("input.txt", "r", stdin);  
        freopen("output.txt", "w", stdout); 
    #endif 

    //Code

    cerr << "time taken : " << (float)clock() / CLOCKS_PER_SEC << " secs" << endl; //Optional
    return 0; 
} """

    return template

def get_filename():
    fileNames = ['A.cpp','B.cpp','C.cpp','D.cpp','E.cpp','F.cpp']
    return fileNames

def get_fn_beginner():
    fileNames = ['A.cpp','B.cpp','C.cpp']
    return fileNames

# Template 2
def template_agg():
    temp = """#pragma GCC optimize("Ofast")
#pragma GCC target("sse,sse2,sse3,ssse3,sse4,popcnt,abm,mmx,avx,avx2,fma")
#pragma GCC optimize("unroll-loops")
#include <bits/stdc++.h> 
#include <complex>
#include <queue>
#include <set>
#include <unordered_set>
#include <list>
#include <chrono>
#include <random>
#include <iostream>
#include <algorithm>
#include <cmath>
#include <string>
#include <vector>
#include <map>
#include <unordered_map>
#include <stack>
#include <iomanip>
#include <fstream>

using namespace std;

typedef long long ll;
typedef long double ld;
typedef pair<int,int> p32;
typedef pair<ll,ll> p64;
typedef pair<double,double> pdd;
typedef vector<ll> v64;
typedef vector<int> v32;
typedef vector<vector<int> > vv32;
typedef vector<vector<ll> > vv64;
typedef vector<vector<p64> > vvp64;
typedef vector<p64> vp64;
typedef vector<p32> vp32;
ll MOD = 998244353;
double eps = 1e-12;
#define forn(i,e) for(ll i = 0; i < e; i++)
#define forsn(i,s,e) for(ll i = s; i < e; i++)
#define rforn(i,s) for(ll i = s; i >= 0; i--)
#define rforsn(i,s,e) for(ll i = s; i >= e; i--)
#define dbg(x) cout<<#x<<" = "<<x<<ln
#define mp make_pair
#define pb push_back
#define fi first
#define se second
#define INF 2e18
#define fast_cin() ios_base::sync_with_stdio(false); cin.tie(NULL); cout.tie(NULL)
#define all(x) (x).begin(), (x).end()
#define sz(x) ((ll)(x).size())


int main()
{
	fast_cin();
    #ifndef ONLINE_JUDGE  
    freopen("in.in", "r", stdin);  
    freopen("out.out", "w", stdout); 
    //Edit names accordingly
    #endif 

	//Code

	return 0;
}
"""
    return temp