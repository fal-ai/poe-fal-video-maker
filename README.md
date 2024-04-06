### This bot uses fly.io as a hosting provider, and fal as an inference provider. 

1) Create a fly account if you don't have one already. New users get $5 credits but you might have to put a credit card. Install the fly command line tools
```
brew install flyctl
```
2) Clone the repository `git clone https://github.com/fal-ai/poe-fal-video-maker`
3) Run `fly launch`
You should get a response like this 

```
[...]
[...]
[...]
--> Pushing image done
image: registry.fly.io/poe-video-maker-hidden-star-1770:deployment-01HTTBCYYYGX897V2XTNF0Z3ZC
image size: 290 MB

Watch your deployment at https://fly.io/apps/poe-video-maker-hidden-star-1770/monitoring

Provisioning ips for poe-video-maker-hidden-star-1770
  Dedicated ipv6: 2a09:8280:1::30:bff9:0
  Shared ipv4: 66.241.124.24
  Add a dedicated ipv4 with: fly ips allocate-v4

This deployment will:
 * create 2 "app" machines

No machines in group app, launching a new machine
Creating a second machine to increase service availability
Finished launching new machines
-------
NOTE: The machines for [app] have services with 'auto_stop_machines = true' that will be stopped when idling

-------
Checking DNS configuration for poe-video-maker-hidden-star-1770.fly.dev

Visit your newly deployed app at https://poe-video-maker-hidden-star-1770.fly.dev/
```
4) Head to the poe website and click "Create Bot" if you haven't done before, and grab your access Access key
   
<img width="874" alt="image" src="https://github.com/fal-ai/poe-fal-video-maker/assets/1714827/e78e2918-d275-4b21-abcf-dae6b68b2e16">

5) Set your Access key as an fly secret 

```
fly secrets set POE_ACCESS_KEY=***
```

6) Head to the fal website and create a fal api key - https://fal.ai/dashboard/keys.
```
fly secrets set FAL_KEY=***
```

7) Run `fly deploy`
You should get a response that ends like this 
```
[...]
[...]
[...]

Reusing cache layer 'paketo-buildpacks/pip:pip'
Reusing cache layer 'paketo-buildpacks/pip-install:cache'
Reusing cache layer 'paketo-buildpacks/pip-install:packages'
Reusing cache layer 'buildpacksio/lifecycle:cache.sbom'
--> Building image done
==> Pushing image to fly
The push refers to repository [registry.fly.io/poe-video-maker-hidden-star-1770]
83d85471d9f8: Layer already exists 
cbbd1d7478e6: Layer already exists 
8812c86dc680: Layer already exists 
1c0b93cba910: Layer already exists 
1d94ce8f370c: Layer already exists 
9ed018058aca: Layer already exists 
b4b70a3d2eaa: Layer already exists 
52efb1a98ceb: Layer already exists 
1eb5983d7301: Layer already exists 
39d381810cef: Layer already exists 
115fc79fb3d1: Layer already exists 
fd93afbbe1ce: Layer already exists 
f92983442b23: Layer already exists 
4d274d05ee12: Layer already exists 
548a79621a42: Layer already exists 
deployment-01HTTC3YB0MZZF7TMR97ZK2T8G: digest: sha256:e3f8c72c4d0d59080a0f06b95e4c4e03101d7e3ddad1e4245db14c6cfca664b0 size: 3453
--> Pushing image done
image: registry.fly.io/poe-video-maker-hidden-star-1770:deployment-01HTTC3YB0MZZF7TMR97ZK2T8G
image size: 290 MB

Watch your deployment at https://fly.io/apps/poe-video-maker-hidden-star-1770/monitoring

-------
Updating existing machines in 'poe-video-maker-hidden-star-1770' with rolling strategy

-------
 ✔ [1/2] Machine 56833d20c22e98 [app] update succeeded
 ✔ [2/2] Machine 6e824792b439d8 [app] update succeeded
-------
Checking DNS configuration for poe-video-maker-hidden-star-1770.fly.dev

Visit your newly deployed app at https://poe-video-maker-hidden-star-1770.fly.dev/
```
7) Now you have a publicly accessible url - https://poe-video-maker-hidden-star-1770.fly.dev. Head to https://poe.com/create_bot?server=1 and follow the instructions to finish creating your bot 
