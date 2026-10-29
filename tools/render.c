/* SPDX-License-Identifier: GPL-3.0-only */
#define main skiff_hostsim_main
#include "../build/firmware/tests/hostsim.c"
#undef main
int main(int argc,char **argv){
 if(argc<6)return 2;
 int pi=atoi(argv[1]),note=atoi(argv[2]),vel=atoi(argv[3]);double secs=atof(argv[4]);
 if(pi<0||pi>=8||note<0||note>127||vel<1||vel>127||secs<.5||secs>60)return 2;
 int wet=argc>7;uint32_t frames=(uint32_t)(secs*FS),release=(uint32_t)((secs-.4)*FS);
 FILE*out=fopen(argv[5],"wb");if(!out)return 3;
 host_tracks_init();host_preset(&trk[0],ENGI_FM6,pi);trk[0].p[P_VOICE]=V_POLY;
 if(argc>6&&strcmp(argv[6],"-")){
  uint8_t p[156]={0};FILE*in=fopen(argv[6],"rb");if(!in){fclose(out);return 3;}
  size_t n=fread(p,1,156,in);fclose(in);if(n!=155){fclose(out);return 4;}
  fm6_set_patch(0,p);fm6_slot[0]=(uint8_t)pi;
 }
 if(!wet)trk[0].p[P_CHOR]=trk[0].p[P_DLY]=trk[0].p[P_REV]=0;
 if(wet)wav_hdr(out,frames);
 static const int chords[4][5]={{48,55,59,62,64},{45,52,55,59,60},{50,57,60,64,65},{43,50,53,57,59}};
 int held[6],nh=0;uint64_t clipped=0;int32_t peak=0;
 for(uint32_t f=0;f<frames;f+=CTL){
  if(!wet&&f==0){trk_note_on(&trk[0],note,vel);held[nh++]=note;}
  if(wet){
   uint32_t period=2*FS,pos=f%period;
   if(pos<CTL){for(int j=0;j<nh;j++)trk_note_off(&trk[0],held[j]);nh=0;
    for(int j=0;j<5;j++){held[nh++]=chords[(f/period)%4][j];trk_note_on(&trk[0],held[nh-1],vel);}}
   if(pos>=FS*3/2&&pos<FS*3/2+CTL){for(int j=0;j<nh;j++)trk_note_off(&trk[0],held[j]);nh=0;}
  }else if(f>=release&&f<release+CTL){for(int j=0;j<nh;j++)trk_note_off(&trk[0],held[j]);nh=0;}
  int32_t b[CTL*2];if(wet)mix_block(b,CTL);else track_render(&trk[0],b,CTL);
  for(uint32_t j=0;j<CTL&&f+j<frames;j++){
   if(wet){int32_t l=b[2*j],r=b[2*j+1];if(l>32767||l< -32768||r>32767||r< -32768)clipped++;
    if(abs(l)>peak)peak=abs(l);if(abs(r)>peak)peak=abs(r);wav_put(out,l,r);
   }else{float x=(float)b[j]/VOICE_FS;fwrite(&x,4,1,out);}
  }
 }
 fclose(out);if(wet)printf("frames=%u peak_pcm=%d clipped_frames=%llu\n",frames,peak,(unsigned long long)clipped);
 return clipped?5:0;
}
