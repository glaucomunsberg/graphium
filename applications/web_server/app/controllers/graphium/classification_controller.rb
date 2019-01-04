class Graphium::ClassificationController < ApplicationController
  respond_to :json, :html, :js
  before_filter :authenticate_user!
  layout "inside"

  def index

  end

  def getInformation

    @informations = {}

    @classifications = []
    if params[:true] == "true"
      @classifications << "T"
    end
    if params[:false] == "true"
      @classifications << "F"
    end

    if params[:true_negative] == "true"
      @classifications << "TN"
    end

    if params[:true_positive] == "true"
      @classifications << "TP"
    end

    if params[:false_negative] == "true"
      @classifications << "FN"
    end

    if params[:false_positive] == "true"
      @classifications << "FP"
    end

    logger.info "Classification wanted"
    logger.info @classifications

    panos = Graphium::Pano.where(:classification.in => @classifications )
    @informations['pano'] = panos[params[:pano_position].to_i]
    @informations['total'] = panos.length
    @informations['classifications'] = @classifications
    respond_to do |format|
      format.json { render :json => @informations }
    end
  end

  def updatePano
    @pano = Graphium::Pano.where(:pano_id => params[:pano_id],:heading => params[:heading]).first
    @pano.classification = params[:pano_classification]
    @pano.save
    if params[:pano_classification] == "FP"
      Graphium::Graffiti.where(:pano_id => params[:pano_id]).each do | graphium |
        if graphium.heading = params[:heading].to_i
          graphium.situation = "false_positive"
          graphium.save
        end
      end
    elsif params[:pano_classification] == "TP"
      Graphium::Graffiti.where(:pano_id => params[:pano_id]).each do | graphium |
        if graphium.heading = params[:heading].to_i
          graphium.situation = "true_positive"
          graphium.save
        end
      end
    end
    respond_to do |format|
      format.json { render :json => @pano }
    end
  end

end
